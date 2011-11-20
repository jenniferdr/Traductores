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
    r'"(\\(?="))*"'
    return t

def t_error(t):
    print "Caracter '%s' no reconocido." % t.value[0]
    t.lexer.skip(1)

lexer= lex.lex()

data= '= 45'

lexer.input(data)

tok=lexer.token()
while (tok):
    print tok #, tok.type,tok.value,tok.lineno,tok.lexpos
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
def p_s(p):
    's : program'

def p_program(p):
    '''program : EQ expresion
             | igual declaraciones'''
    print "program igual dec"
     

def p_empty(p):
    'empty : '
    pass

def p_igual_salida(p):
    '''igual : EQ
             | empty'''
    print "="

def p_declaraciones(p):
    '''declaraciones : VAR COLON type COMMA declaraciones COMMA expresion
                     | VAR COLON type ASIG expresion '''
    print "declaracion"

def p_type(p):
    ''' type : INT
             | TSTRING
             | LISTOF INT 
             | LISTOF TSTRING
             | TABLE '''
    print "tipo"

def p_expresion(p):
    ''' expresion : operando
                  | tabla
                  | INPUT '''
    print "expresion"

def p_operando(p):
    ''' operando : operando operador aux
                 | operando FBY aux
                 | opTby
                 | aux '''
    print "operando"

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
    print "aux"

def p_m(p):
    ''' m : MINUS %prec UMINUS
          | NOT %prec UNOT
		  | empty'''

def p_cuant(p):
    'cuant : LLIST cuan VAR COLON operando COLON operando RLIST'

def p_list(p):
    '''list : LLIST VAR COLON operando COLON operando RLIST
            | LBRACK expList RBRACK'''
    print "list"

def p_cuan(p):
    '''cuan : operador
            | opBool'''

def p_operador(p):
    '''operador : PLUS
                | MINUS
                | TIMES
                | MOD
                | POW
                | DIV'''

def p_expList(p):
    '''expList : expList COMMA operando
               | operando'''
    if(len(p)==2):
        print "expList , operando"
    else:
        print "operando"

def p_opTby(p):
    'opTby : operando TBY LBRACK listVars RBRACK'

def p_listVars(p):
    '''listVars : listVars COMMA VAR
                | VAR'''

def p_select(p):
    'select : IF expBool THEN expresion ELSE expresion'

def p_comp(p):
    '''comp : GT
            | LT
            | LTE
            | GTE
            | EQ
            | NOTEQ '''

def p_expBool(p):
    '''expBool : expBool opBool condExp
               | condExp
               | m LPAREN expBool RPAREN '''

def p_opBool(p):
    ''' opBool : AND
               | OR '''

def p_condExp(p):
    '''condExp : operando comp operando
               | m LPAREN condExp RPAREN
               | m cuant
               | m TRUE
               | m FALSE '''

#def p_neg(p):
#    '''neg : NOT %prec UNOT
#           | empty '''
 
def p_tabla(p):
    'tabla : NEWTABLE LBRACK operando RBRACK WHERE col'

def p_col(p):
    ''' col : VAR COLON typ ASIG val
            | col SEMICOLON VAR COLON typ ASIG val'''

def p_typ(p):
    '''typ : INT
           | TSTRING'''

def p_val(p):
    '''val : operando
           | INPUT '''
    print "operando o input"
		   
def p_error(p):
    print "Syntax error in input! %s" % p

parser = yacc.yacc(start='s')

result = parser.parse(data)
print result
