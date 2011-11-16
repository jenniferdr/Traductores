# --------------------------------------------------
# Analizador lexicografico para el lenguaje ShinyEl
# 
# Autores : Hancel Gonzalez   07-40983
#           Jennifer Dos Reis 08-10323
#
# --------------------------------------------------

tokens= ('NUM','VAR','STRING','QUOT','LBRACK','RBRACK','MINUS'
         'COLON', 'RLIST','LLIST','COMMA','INT','LISTOF','TSTRING'
         'TABLE','NEWTABLE','WHERE','EQ','ASIG','PLUS',
         'TIMES','DIV','MOD','POW','IF','THEN','ELSE',
         'AND','OR','NOT','NOTEQ','LT','GT','GTE','LTE','TRUE',
         'FALSE','FBY','TBY','RPAREN','LPAREN','DOT','LEN',
         'INPUT','RANGE','SEMICOLON'
         )
# ER de cada Token

t_NUM=     r'[0-9]+'
t_VAR=     r'[a-zA-Z][a-zA-Z0-9_]*'
t_STRING=  r''
t_QUOT=    r'"'
t_LBRACK=  r'['
t_RBRACK=  r']'
t_MINUS=   r'-'
t_COLON=   r':'
t_RLIST=   r'%]'
t_LLIST=   r'[%'
t_COMMA=   r','
t_INT=     r'int'
t_TSTRING= r'string'
t_LISTOF=  r'list of'
t_TABLE=   r'table'
t_NEWTABLE=r'new table'
t_WHERE=   r'where'
t_EQ=      r'='
t_ASIG=    r':='
t_PLUS=    r'\+'
t_TIMES=   r'\*'
t_DIV=     r'/'
t_MOD=     r'%'
t_POW=     r'\*\*'
t_IF=      r'if'
t_THEN=    r'then'
t_ELSE=    r'else'
t_AND=     r'&'
t_OR=      r'|'
t_NOT=     r'!'
t_NOTEQ=   r'!='
t_LT=      r'<'
t_GT=      r'>'
t_LTE=     r'<='
t_GTE=     r'>='
t_TRUE=    r'true'
t_FALSE=   r'false'
t_FBY=     r'fby'
t_TBY=     r'tby'
t_RPAREN=  r')'
t_LPAREN=  r'('
t_DOT=     r'\.'
t_LEN=     r'len'
t_INPUT=   r'input'
t_RANGE=   r'range'
t_SEMICOLON= r';'
