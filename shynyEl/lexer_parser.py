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
    'list': 'LIST',
    'of': 'OF',
    'table':'TABLE',
    'new':'NEW',
    'table':'TABLE',    
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
    r'"([^"\\]|\\"|\\\\|\n|\t|\r|\f|\v)*"'
    t.value= (t.value)[1:-1]
    return t

def t_error(t):
    print "Caracter '%s' no reconocido." % t.value[0]
    t.lexer.skip(1)

lexer = lex.lex()

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

class Expresion: pass

class BinOp(Expresion):
    def __init__(self,op1,op2):
        self.op1 = op1
        self.op2 = op2

class Suma(BinOp):
    def __str__(self):
        return "Suma(" + str(self.op1) + "," + str(self.op2) + ")"

class Resta(BinOp):
    def __str__(self):
        return "Resta(" + str(self.op1) + "," + str(self.op2) + ")"

class Producto(BinOp):
    def __str__(self):
        return "Producto(" + str(self.op1) + "," + str(self.op2) + ")"

class Division(BinOp):
    def __str__(self):
        return "Division(" + str(self.op1) + "," + str(self.op2) + ")"

class Mod(BinOp):
    def __str__(self):
        return "Mod(" + str(self.op1) + "," + str(self.op2) + ")"

class Potencia(BinOp):
    def __str__(self):
        return "Potencia(" + str(self.op1) + "," + str(self.op2) + ")"

class Fby(BinOp):
    def __str__(self):
        return "Fby(" + str(self.op1) + "," + str(self.op2) + ")"

class And(BinOp):
    def __str__(self):
        return "And(" + str(self.op1) + "," + str(self.op2) + ")"

class Or(BinOp):
    def __str__(self):
        return "Or(" + str(self.op1) + "," + str(self.op2) + ")"

class MayorQue(BinOp):
    def __str__(self):
        return "MayorQue(" + str(self.op1) + "," + str(self.op2) + ")"

class MenorQue(BinOp):
    def __str__(self):
        return "MenorQue(" + str(self.op1) + "," + str(self.op2) + ")"

class MayorIgualQue(BinOp):
    def __str__(self):
        return "MayorIgualQue(" + str(self.op1) + "," + str(self.op2) + ")"

class MenorIgualQue(BinOp):
    def __str__(self):
        return "MenorIgualQue(" + str(self.op1) + "," + str(self.op2) + ")"

class Igual(BinOp):
    def __str__(self):
        return "Igual(" + str(self.op1) + "," + str(self.op2) + ")"
    
class Distinto(BinOp):
    def __str__(self):
        return "Distinto(" + str(self.op1) + "," + str(self.op2) + ")"    

class UnOp(Expresion):
    def __init__(self,op):
        self.op = op

class Neg(UnOp):
    def __str__(self):
        return "Neg(" + str(self.op) +")"

class Min(UnOp):
    def __str__(self):
        return "Min(" + str(self.op) +")"    

class TbyOp(BinOp):
    def __str__(self):
        return  "TbyOp(" + str(self.op1) + "," + str(self.op2) + ")"

class IfExp(Expresion):
    def __init__(self,cond,exp1,exp2):
        self.cond = cond
        self.exp1 = exp1
        self.exp2 = exp2
        
    def __str__(self):
        return  "IfExp(" + str(self.cond) + "," + str(self.exp1) + "," + str(self.exp2) + ")"

class AccList(Expresion):
    def __init__(self,var,index):
        self.var = var
        self.index = index

    def __str__(self):
        return "AccList(" + self.var + "," + str(self.index) + ")"

class AccTab(Expresion):
    def __init__(self,var,col,index):
        self.var = var
        self.col = col
        self.index = index

    def __str__(self):
        return "AccTab(" + str(self.var) + "," + self.col + "," + str(self.index) + ")"

class Salida:
    def __init__(self,exp):
        self.exp = exp

    def __str__(self):
        aux = '['
        for exp in self.exp:
            aux = aux + str(exp) + ','
        aux = aux[:-1] + ']'

        return "Salida(" + aux + ")"
		
class Tabla(Expresion):
    def __init__(self,tam,col):
        self.tam = tam
        self.col = col

    def __str__(self):
        aux = '['
        for c in self.col:
            aux = aux + '(' + str(c.var) + ',' + str(c.type) + ',' + str(c.exp) + ')' + ','
        aux = aux[:-1] + ']'
        
        return "Tabla(" + str(self.tam) + "," + aux + ")"

class ColTabla:
    def __init__(self,var,type,exp):
        self.var = var
        self.type = type
        self.exp = exp

    def __str__(self):
        return "ColTabla(" +str( self.var) + "," + self.type + "," + str(self.exp) + ")"
		
class Range(Expresion):
    def __init__(self,ini,fin):
        self.ini = ini
        self.fin = fin

    def __str__(self):
        return "Range(" + str(self.ini) + "," + str(self.fin) + ")"

class Len(Expresion):
    def __init__(self,var):
        self.var = var

    def __str__(self):
        return "Len(" + str(self.var) + ")"
		
class NoSalida:
    def __init__(self,exp):
        self.exp = exp

    def __str__(self):
        aux = '['
        for exp in self.exp:
            aux = aux + str(exp) + ','
        aux = aux[:-1] + ']'

        return "NoSalida(" + aux + ")"

class SalidaExpresion:
    def __init__(self,exp):
        self.exp = exp

    def __str__(self):
        return "NoSalida(" + str(self.exp) + ")"

class Dec:
    def __init__(self,vars,typs,exps):
        self.vars = vars
        self.typs = typs
        self.exps = exps

    def __str__(self):
        return "Dec(" + str(self.vars) + "," + str(self.typs) + "," + str(self.exps) + ")"
		
class Cuant(Expresion):
    def __init__(self,op,var,list,exp):
        self.op = op
        self.var = var
        self.list = list
        self.exp = exp

    def __str__(self):
        return "Cuant(" + str(self.op) + "," + str(self.var) + "," + str(self.list) + "," + str(self.exp) + ")"

class List(Expresion):
    def __init__(self,list):
        self.list =  list

    def __str__(self):
        return "List(" + str(self.list) + ")"

#######################################################
#####   Reglas o Producciones de la Gramatica  ########
#######################################################

def p_program_dec(p):
    '''program : EQ declaraciones
               | declaraciones'''
    if len(p) == 3:
        j = 2
    else:
        j = 1
        
    p[j][2].reverse()
    aux = []
    for i,var in enumerate(p[j][0]):
        aux.append(Dec(var,p[j][1][i],p[j][2][i]))
        if isinstance(p[j][2][i],Tabla):
            col = p[j][2][i].col
            simb_tabletype = {}
            for c in col:
                simb_tabletype[c.var] = (c.type,c.exp)
            nombres[var] = (p[j][1][i],simb_tabletype)    
        else:
            nombres[var] = (p[j][1][i],p[j][2][i])
        
    if len(p) == 3:
        p[0] = Salida(aux)
    else:
        p[0] = NoSalida(aux)
       
def p_program_exp(p):
    'program : EQ expresion'
    p[0] = SalidaExpresion(p[2])
    
def p_empty(p):
    'empty :'
    p[0] = ''
    pass
    
#def p_igual_salida(p):
#    '''igual : EQ
#             | empty'''
#    p[0] = p[1]
    
def p_declaraciones(p):
    '''declaraciones : VAR COLON type COMMA declaraciones COMMA expresion
                     | VAR COLON type ASIG expresion ''' 
    if len(p) == 6:
        p[0] = ([p[1]],[p[3]],[p[5]])
    else:
        p[5][0].append(p[1])
        p[5][1].append(p[3])
        p[5][2].append(p[7])
        p[0] = p[5]

def p_type(p):
    ''' type : typ
             | LIST OF typ 
             | TABLE '''
    if len(p) == 4:
        p[0] = p[1] + ' ' + p[2] + ' ' + p[3]
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
        if p[2] == '+':
            p[0] = Suma(p[1],p[3])
        elif p[2] == '-':
            p[0] = Resta(p[1],p[3])
        elif p[2]== '*':
            p[0] = Producto(p[1],p[3])
        elif p[2] == '/':
            p[0] = Division(p[1],p[3])
        elif p[2] == '%':
            p[0] = Mod(p[1],p[3])
        elif p[2] == '**':
            p[0] = Potencia(p[1],p[3])
        elif p[2] == 'fby' :
            p[0] = Fby(p[1],p[3])
    else:
        p[0] = p[1]

def p_aux(p):
    ''' aux : NUM
            | VAR
            | m LPAREN operando RPAREN
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
        if p[2] == '(':
            p[0] = Range(p[3],p[5])
        if p[2] == '[':
            p[0] = AccTab(p[1],p[6],p[3])
    elif len(p) == 5:
        if p[2] == '(':
            if p[1] == 'len':
                p[0] = Len(p[3])
            else:
                if p[1] == '-':
                    p[0] = Min(p[3])
                else:
                    p[0] = p[3]
        elif p[2] == '[':
            p[0] = AccList(p[1],p[3])
    elif len(p) == 4:
        p[0] = AccTab(p[1],p[3],0)
    elif len(p) == 3:
        p[0] = Min(p[2])
    else:
        p[0] = p[1]    

def p_m(p):
    ''' m : MINUS %prec UMINUS
          | NOT %prec UNOT
          | empty'''
    p[0] = p[1]
    
def p_cuant(p):
    'cuant : LLIST cuan VAR COLON operando COLON operando RLIST'
    p[0] = Cuant(p[2],p[3],p[5],p[7])
    
def p_list(p):
    '''list : LLIST VAR COLON operando COLON operando RLIST
            | LBRACK expList RBRACK'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = Cuant('',p[2],p[4],p[6])
    
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
               | operando
               | empty'''
    if len(p) == 2:
        if p[1] == '':
            p[0] = []
        else:
            p[0] = List([p[1]])
    else:
        p[1].list.append(p[3])
        p[0] = p[1]

def p_opTby(p):
    'opTby : operando TBY LBRACK listVars RBRACK'
    p[0] = TbyOp(p[1],p[4])

def p_listVars(p):
    '''listVars : listVars COMMA VAR
                | VAR'''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
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
        if p[1] == '!':
            p[0] = Neg(p[3])
        else:
            p[0] = p[3]
    elif len(p) == 4:
        if p[2] == '&':
            p[0] = And(p[1],p[3])
        elif p[2] == '|':
            p[0] = Or(p[1],p[3])
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
        if p[1] == '!':
            p[0] = Neg(p[3])
        else:
            p[0] = p[3]        
    elif len(p) == 4:
        if p[2] == '=':
            p[0] = Igual(p[1],p[3])
        elif p[2] == '!=':
            p[0] = Distinto(p[1],p[3])
        elif p[2] == '>':
            p[0] = MayorQue(p[1],p[3])
        elif p[2] == '<':
            p[0] = MenorQue(p[1],p[3])
        elif p[2] == '>=':
            p[0] = MayorIgualQue(p[1],p[3])
        elif p[2] == '<=':
            p[0] = MenorIgualQue(p[1],p[3])
    else:
        if p[1] == '!':
            p[0] = Neg(p[2])
        else:
            p[0] = p[2]

def p_tabla(p):
    'tabla : NEW TABLE LBRACK operando RBRACK WHERE col'
    p[0] = Tabla(p[4],p[7])

def p_col(p):
    ''' col : VAR COLON typ ASIG expresion
            | col SEMICOLON VAR COLON typ ASIG expresion'''
    if len(p) == 8:
        p[1].append(ColTabla(p[3],p[5],p[7]))
        p[0] = p[1]
    else:
        p[0] = [ColTabla(p[1],p[3],p[5])]

def p_typ(p):
    '''typ : INT
           | TSTRING'''
    p[0] = p[1]


def p_error(p):
    print "Syntax error in input! %r" % p.value

parser = yacc.yacc(start='program')