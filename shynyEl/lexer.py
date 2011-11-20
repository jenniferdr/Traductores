# --------------------------------------------------
# Analizador lexicografico para el lenguaje ShinyEl
# 
# Autores : Hancel Gonzalez   07-40983
#           Jennifer Dos Reis 08-10323
#
# --------------------------------------------------
import ply.lex as lex
import ply.yacc as yacc
import sys
import clases

reserved= {
    'int': 'INT',
    'string':'TSTRING',
    'list of': 'LISTOF',
    'table':'TABLE',
    'new table':'NEWTABLE',
    'where':'WHERE',
    'if':'IF',
    'then':'THEN',
    'else':'ELSE',
    'true':'TRUE',
    'false':'FALSE',
    'fby':'FBY',
    'tby':'TBY',
    'len':'LEN',
    'input':'INPUT',
    'range':'RANGE'    
    }

tokens= ['NUM','VAR','STRING','LBRACK','RBRACK','MINUS',
         'COLON', 'RLIST','LLIST','COMMA','EQ','ASIG','PLUS',
         'TIMES','DIV','MOD','POW','AND','OR','NOT','NOTEQ','LT',
         'GT','GTE','LTE','RPAREN','LPAREN','DOT','SEMICOLON',
        ] + list(reserved.values())

# ER de cada Token

#t_QUOT=    r'"'
t_LBRACK=  r'\['
t_RBRACK=  r'\]'
t_MINUS=   r'-'
t_COLON=   r':'
t_RLIST=   r'%\]'
t_LLIST=   r'\[%'
t_COMMA=   r','
t_EQ=      r'='
t_ASIG=    r':='
t_PLUS=    r'\+'
t_TIMES=   r'\*'
t_DIV=     r'/'
t_MOD=     r'%'
t_POW=     r'\*\*'
t_AND=     r'&'
t_OR=      r'\|'
t_NOT=     r'!'
t_NOTEQ=   r'!='
t_LT=      r'<'
t_GT=      r'>'
t_LTE=     r'<='
t_GTE=     r'>='
t_RPAREN=  r'\)'
t_LPAREN=  r'\('
t_DOT=     r'\.'
t_SEMICOLON= r';'     
t_ignore_WHITESPACES= r'\s+'

def t_VAR(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type= reserved.get(t.value,'VAR')
    return t

def t_NUM(t):
    r'\d+'
    try:
        t.value=int(t.value)
    except ValueError:
        print("Entero muy largo %d",t.value)
    return t

def t_STRING(t):
    r'"([^"]|\")*"'
    return t

def t_error(t):
    print "Caracter '%s' no reconocido." % t.value[0]
    t.lexer.skip(1)

lexer= lex.lex()

data= sys.argv[1]

lexer.input(data)

tok=lexer.token()
while (tok):
    #print tok #, tok.type,tok.value,tok.lineno,tok.lexpos
    tok=lexer.token()

# Reglas o Producciones de la Gramatica

precedence = (
    ('left','AND','OR'),
	('right','UNOT'),
	('nonassoc','LT','LTE','GT','GTE'),
	('nonassoc','EQ','NOTEQ'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIV','MOD'),
    ('right','UMINUS'),
    )

nombres={}

def p_program(p):
    'program : igual declaraciones'
    '        | EQ expresion'
    if p[1] == '=':
        p[0] = Salida(p[2])
    else:
        p[0] = Program(p[2])
	
def p_empty(p):
    'empty :'
    p[0] = ''
    pass
	
def p_igual_salida(p):
    '''igual : EQ
             | empty'''
    p[0] = p[1]
	
def p_declaraciones(p):
    '''declaraciones : VAR COLON type COMMA declaraciones COMMA expresion
                     | VAR COLON type ASIG expresion ''' 
    if len(p) == 6:
	    p[0] = [Dec(p[3],p[5])]
    else:
        p[0] = p[5].extend([Dec(p[3],p[7])])

def p_type(p):
    ''' type : INT
             | TSTRING
             | LISTOF INT 
             | LISTOF TSTRING
             | TABLE '''
    if len(p) == 3:
	    p[0] = p[1] + ' ' + p[2]
    else:
	    p[0] = p[1]

def p_expresion(p):
    ''' expresion : operando
                  | tabla
                  | INPUT'''
    p[0] = p[1]

def p_operando(p):
    ''' operando : operando operador aux
                 | operando FBY aux
                 | opTby
                 | aux '''
    if len(p) == 4:
        p[0] = BinOp(p[1],p[2],p[3])
    else:
        p[0] = p[1]	

def p_aux(p):
    ''' aux : NUM
            | VAR
            | m LPAREN operando RPAREN %prec UMINUS
            | MINUS aux %prec UMINUS
            | STRING
            | list
            | select 
            | cuant
            | VAR LBRACK operando RBRACK
            | VAR LBRACK operando RBRACK DOT VAR
            | VAR DOT VAR 
            | LEN LPAREN operando RPAREN 
            | RANGE LPAREN operando COMMA operando RPAREN '''
    if len(p) == 7:
	    if p[2] = '(':
            p[0] = Range(p[3],p[5])
	    if p[2] = '[':
            p[0] = AccTab(p[1],p[6],p[3])
    elif len(p) == 5:
        p[0] = UnOp(p[1],p[3])
    elif len(p) == 4:
	    if p[2] = '(':
            p[0] = UnOp(p[1],p[3])
	    if p[2] = '[':
            p[0] = AccList(p[1],p[3])
    elif len(p) == 3:
        p[0] = UnOp(p[1],p[2])
    else:
	    p[0] = Ctte(p[1])
		
def p_m(p):
    ''' m : MINUS %prec UMINUS
          | NOT %prec UNOT
		  | empty'''
        p[0] = p[1]

def p_cuant(p):
    'cuant : LLIST cuan VAR COLON operando COLON operando RLIST'
    p[0] = Cuan(p[2],p[3],p[5],p[7])

def p_list(p):
    '''list : LLIST VAR COLON operando COLON operando RLIST
            | LBRACK expList RBRACK'''
    if len(p) == 4:
        p[0] = p[1] + p[2] + p[3]
    else:
        p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6] + p[7]

def p_cuan(p):
    '''cuan : operador
            | opBool'''
    p[0] = p[1]

def p_operador(p):
    '''operador : PLUS
                | MINUS
                | TIMES
                | MOD
                | POW
                | DIV'''
    p[0] = p[1]

def p_expList(p):
    '''expList : expList COMMA operando
               | operando'''
    if len(p) == 2:
        p[0] = [p[1]]	
    else:
        p[0] = p[1].extend([p[3]])

def p_opTby(p):
    'opTby : operando TBY LBRACK listVars RBRACK'
    p[0] = p[1] + p[2] + p[3] + p[4] + p[5]

def p_listVars(p):
    '''listVars : listVars COMMA VAR
                | VAR'''
    if len(p) == 4:
        p[0] = p[1].append(p[3])
    else:
        p[0] = [p[1]]

def p_select(p):
    'select : IF expBool THEN expresion ELSE expresion'
    p[0] = IfExp(p[2],p[4],p[6])	

def p_comp(p):
    '''comp : GT
            | LT
            | LTE
            | GTE
            | EQ
            | NOTEQ '''
    p[0] = p[1]	

def p_expBool(p):
    '''expBool : expBool opBool condExp
               | condExp
               | m LPAREN expBool RPAREN '''
    if len(p) == 5:
        p[0] = p[1] + p[2] + p[3] + p[4]
    elif len(p) == 4:
        p[0] = p[1] + p[2] + p[3]
    else:
        p[0] = p[1]	

def p_opBool(p):
    ''' opBool : AND
               | OR '''
    p[0] = p[1]			   

def p_condExp(p):
    '''condExp : operando comp operando
               | m LPAREN condExp RPAREN
               | m cuant
               | m TRUE
               | m FALSE '''
    if len(p) == 5:
        p[0] = p[1] + p[2] + p[3] + p[4]
    elif len(p) == 4:
        p[0] = p[1] + p[2] + p[3]
    else:
        p[0] = UnOp(p[1],p[2])

#def p_neg(p):
#    '''neg : NOT %prec UNOT
#           | empty '''
 
def p_tabla(p):
    'tabla : NEWTABLE LBRACK operando RBRACK WHERE col'
    p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6]

def p_col(p):
    ''' col : VAR COLON typ ASIG val
            | col SEMICOLON VAR COLON typ ASIG val'''
    if len(p) == 8:
        p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6] + p[7]
    else:
        p[0] = p[1] + p[2] + p[3] + p[4] + p[5]	

def p_typ(p):
    '''typ : INT
           | TSTRING'''
    p[0] = p[1]		   

def p_val(p):
    '''val : operando
           | INPUT '''
    p[0] = p[1]		   
		   
def p_error(p):
    print "Syntax error in input! %r" % p.value

parser = yacc.yacc(start='program')

print parser.parse(data)