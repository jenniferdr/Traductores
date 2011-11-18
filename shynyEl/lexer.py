# --------------------------------------------------
# Analizador lexicografico para el lenguaje ShinyEl
# 
# Autores : Hancel Gonzalez   07-40983
#           Jennifer Dos Reis 08-10323
#
# --------------------------------------------------
import ply.lex as lex
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

tokens= ['NUM','VAR','STRING','QUOT','LBRACK','RBRACK','MINUS',
         'COLON', 'RLIST','LLIST','COMMA','EQ','ASIG','PLUS',
         'TIMES','DIV','MOD','POW','AND','OR','NOT','NOTEQ','LT',
         'GT','GTE','LTE','RPAREN','LPAREN','DOT','SEMICOLON',
         'WHITESPACES'] + list(reserved.values())

# ER de cada Token

t_QUOT=    r'"'
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
    print tok, tok.type,tok.value,tok.lineno,tok.lexpos
    tok=lexer.token()

# Reglas o Producciones de la Gramatica

nombres={ }

 
def p_program(t):
    'program : igual declaraciones'
    '        | igual expresion'
    
def p_empty(p):
    'empty : '
    pass

def p_igual_salida(t):
    '''igual : EQ
       | empty'''

def p_declaraciones(t):
    '''declaraciones :
          VAR COLON type COMMA declaraciones COMMA expresion
          | VAR COLON type ASIG expresion '''

def p_type(t):
    ''' type : INT
             | STRING
             | LISTOF INT 
             | LISTOF STRING
             | TABLE '''

def p_expresion(t):
    ''' expresion : operando
                  | tabla
                  | INPUT '''

def p_operando(t):
    ''' operando : operando operador aux
                 | operando FBY aux
                 | opTby
                 | aux '''

def p_aux(t):
    ''' aux : NUMBER
            | VAR
            | m LPAREN operando RPAREN
            | MINUS aux
            | STRING
            | list
            | select 
            | cuant
            | VAR LBRACK operando RBRACK
            | VAR LBRACK operando RBRACK DOT VAR
            | VAR DOT VAR 
            | LEN LPAREN operando RPAREN 
            | RANGE LPAREN orerando COMMA operando RPAREN
            '''

def p_cuant(t):
    'cuant : LLIST cuan VAR COLON operando COLON operando RLIST'
# Aqui falta que se pueda iterar por una tabla 

def p_list(t):
     'list : LLIST VAR COLON operando COLON operando RLIST'
     '     | LBRACK expList RBRACK'
# Aqui tambien 
def p_cuan(t):
    '''cuan : operando
            | operandoBool'''

def p_operando(t):
    '''operando : PLUS
                | MINUS
                | TIMES
                | MOD
                | POW
                | DIV ''' 

def p_expList(t):
    '''expList : expList COMMA operando
               | operando'''

def p_opTby(t):
    'operando TBY vars'

def p_vars(t):
    
