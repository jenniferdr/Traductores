# --------------------------------------------------------------
# Analizador lexicografico y sintactico para el lenguaje ShinyEl
# 
# Autores : Hancel Gonzalez   07-40983
#           Jennifer Dos Reis 08-10323
#
# ---------------------------------------------------------------
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
    r'"([^"\\]|\\"|\\\\|\\n|\\t|\\r|\\f|\\v)*"'
    t.value= (t.value)[1:-1]
    return t

def t_error(t):
    print "Caracter '%s' no reconocido." % t.value[0]
    t.lexer.skip(1)

precedence = (
    ('left','IF','THEN','ELSE'),
    ('left','AND','OR'),
    ('right','UNOT'),
    ('left','TBY'),
    ('right','FBY'),
    ('nonassoc','LT','LTE','GT','GTE'),
    ('nonassoc','EQ','NOTEQ'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIV','MOD'),
    ('right','UMINUS'),
    )

###########################################################################
#########   CLASES PARA REPRESENTACION DEL ARBOL SINTACTICO ###############
###########################################################################

def html_input_js(id,eval):
    return '<input type = "text" id = "sel_' + id + '" onchange="eval_' + eval + '();" ' + 'value="0"/>'

def html_input(id):
    return '<input type = "text" id = "sel_' + id + '" value="0"/>'

def html_span(id):
    return '<span id = "sel_' + id + '"></span>'

class SalidaNoSalida:
    def __init__(self,exp):
        if isinstance(exp,list):
            exp.reverse()
            self.exp = exp
        else:
            self.exp = exp

class Salida(SalidaNoSalida):
    def __str__(self):
        aux = '['
        for exp in self.exp:
            aux = aux + str(exp) + ','
        aux = aux[:-1] + ']'

        return "Salida(" + aux + ")"

    def html(self):
        aux = []
        for exp in self.exp:
            aux.append(exp.html())
        return aux

class NoSalida(SalidaNoSalida):
    def __str__(self):
        aux = '['
        for exp in self.exp:
            aux = aux + str(exp) + ','
        aux = aux[:-1] + ']'

        return "NoSalida(" + aux + ")"

    def html(self):
        return ''

class SalidaExpresion(SalidaNoSalida):
    def __str__(self):
        return "SalidaExpresion(" + str(self.exp) + ")"

    def html(self):
        return ''

class Dec:
    def __init__(self,var,type,exp):
        self.var = var
        self.type = type
        self.exp = exp

    def __str__(self):
        return "Dec(" + str(self.var) + "," + str(self.type) + "," + str(self.exp) + ")"

    def eval(self):
        if "list of" in self.type:
            if isinstance(self.exp,List):
                tmp = ''
                for i,e in enumerate(self.exp.list):
                    tmp = tmp + 'variables["' + self.var.var + '"]["' + str(i) + '"] = '+  e.eval() + ';\n\t'
                return tmp[:-2]
            elif isinstance(self.exp,Cuant):
                return "codigo js de un cuantificador"
        elif self.type == "table":
            return "codigo js de una tabla"
        else:
            if self.exp != "input":
                if not(isinstance(self.exp,Cuant)):
                    return 'variable["' + self.var.var + '"] = ' + self.exp.eval() + ";"
            else:
                tmp = 'document.getElementById("sel_' + self.var.var + '").value'
                if self.type == 'int':
                    return self.var.eval() + ' = parseInt(' + tmp + ');'
                elif self.type == 'string':
                    return self.var.eval() + ' = ' + tmp + ';'

    def html(self):
        tmp = ''
        if self.type == 'table':
            tmp = tmp + '<table>\n'
            for i in range(0,self.exp.tam):
                tmp = tmp + '    <tr>'
                for c in self.exp.col:
                    tmp = tmp + '\n        <td>'
                    id = self.var.var + '_' + str(i) + '_' + c.var.var
                    if c.exp == 'input':
                        tmp = tmp + html_input_js(id,self.var.var + '_' + c.var.var)
                    else:
                        tmp = tmp + html_span(id)
                    tmp = tmp + '</td>'
                tmp = tmp + '\n    </tr>\n'
            tmp = tmp + '</table>\n'
        elif 'list of' in self.type:
            ## if self.type == 'list of':
            ##     return "Lista Vacia"
            if isinstance(self.exp,List):
                l = len(self.exp.list)
                for i in range(0,l):
                    tmp = tmp + html_span(self.var.var + '_' + str(i)) + ','
                    tmp = tmp[:-1]

        else:
            if self.exp == 'input':
                tmp = html_input_js(self.var.var,self.var.var)
            else:
                tmp = html_span(self.var.var)
        return tmp

class Expresion:
    def __init__(self,tipo=None):
        self.tipo= tipo

class BinOp(Expresion):
    def __init__(self,op1,op2):
        Expresion.__init__(self)
        self.op1 = op1
        self.op2 = op2

class Suma(BinOp):
    def __str__(self):
        return "Suma(" + str(self.op1) + "," + str(self.op2) + ")"

    def eval(self):
        return "(" + self.op1.eval() + " + " + self.op2.eval() + ")"

class Resta(BinOp):
    def __str__(self):
        return "Resta(" + str(self.op1) + "," + str(self.op2) + ")"

    def eval(self):
        return "(" + self.op1.eval() + " - " + self.op2.eval() + ")"		

class Producto(BinOp):
    def __str__(self):
        return "Producto(" + str(self.op1) + "," + str(self.op2) + ")"

    def eval(self):
        return "(" + self.op1.eval() + " * " + self.op2.eval() + ")"		

class Division(BinOp):
    def __str__(self):
        return "Division(" + str(self.op1) + "," + str(self.op2) + ")"

    def eval(self):
        return "(" + self.op1.eval() + " / " + self.op2.eval() + ")"		

class Mod(BinOp):
    def __str__(self):
        return "Mod(" + str(self.op1) + "," + str(self.op2) + ")"

    def eval(self):
        return "(" + self.op1.eval() + " % " + self.op2.eval() + ")"

class Potencia(BinOp):
    def __str__(self):
        return "Potencia(" + str(self.op1) + "," + str(self.op2) + ")"

    def eval(self):
        return "Math.pow(" + self.op1.eval() + "," + self.op2.eval() + ")"

class Fby(BinOp):
    def __str__(self):
        return "Fby(" + str(self.op1) + "," + str(self.op2) + ")"

class TbyOp(BinOp):
    def __str__(self):
        return  "TbyOp(" + str(self.op1) + "," + str(self.op2) + ")"

class OpBool(BinOp):
    pass

class And(OpBool):
    def __str__(self):
        return "And(" + str(self.op1) + "," + str(self.op2) + ")"

    def eval(self):
        return "(" + self.op1.eval() + " && " + self.op2.eval() + ")"

class Or(OpBool):
    def __str__(self):
        return "Or(" + str(self.op1) + "," + str(self.op2) + ")"

    def eval(self):
        return "(" + self.op1.eval() + " || " + self.op2.eval() + ")"

class Comparacion(BinOp):
    pass

class MayorQue(Comparacion):
    def __str__(self):
        return "MayorQue(" + str(self.op1) + "," + str(self.op2) + ")"

    def eval(self):
        return "(" + self.op1.eval() + " > " + self.op2.eval() + ")"

class MenorQue(Comparacion):
    def __str__(self):
        return "MenorQue(" + str(self.op1) + "," + str(self.op2) + ")"

    def eval(self):
        return "(" + self.op1.eval() + " < " + self.op2.eval() + ")"		

class MayorIgualQue(Comparacion):
    def __str__(self):
        return "MayorIgualQue(" + str(self.op1) + "," + str(self.op2) + ")"

    def eval(self):
        return "(" + self.op1.eval() + " >= " + self.op2.eval() + ")"		

class MenorIgualQue(Comparacion):
    def __str__(self):
        return "MenorIgualQue(" + str(self.op1) + "," + str(self.op2) + ")"

    def eval(self):
        return "(" + self.op1.eval() + " <= " + self.op2.eval() + ")"		

class Igual(Comparacion):
    def __str__(self):
        return "Igual(" + str(self.op1) + "," + str(self.op2) + ")"

    def eval(self):
        return "(" + self.op1.eval() + " == " + self.op2.eval() + ")"

class Distinto(Comparacion):
    def __str__(self):
        return "Distinto(" + str(self.op1) + "," + str(self.op2) + ")"    

    def eval(self):
        return "(" + self.op1.eval() + " != " + self.op2.eval() + ")"		

class UnOp(Expresion):
    def __init__(self,op):
        Expresion.__init__(self)
        self.op = op

class Neg(UnOp):
    def __str__(self):
        return "Neg(" + str(self.op) +")"

    def eval(self):
        return "!(" + self.op.eval() + ")"

class Min(UnOp):
    def __str__(self):
        return "Min(" + str(self.op) +")"    

    def eval(self):
        return "-(" + self.op.eval() + ")"		

class IfExp(Expresion):
    def __init__(self,cond,exp1,exp2):
        Expresion.__init__(self)
        self.cond = cond
        self.exp1 = exp1
        self.exp2 = exp2

    def __str__(self):
        return  "IfExp(" + str(self.cond) + "," + str(self.exp1) + "," + str(self.exp2) + ")"

    def eval(self):
        return "(" + self.cond.eval() + "?" + self.exp1.eval() + ":" + self.exp2.eval() + ")"

class AccList(Expresion):
    def __init__(self,var,index):
        Expresion.__init__(self)
        self.var = var
        self.index = index

    def __str__(self):
        return "AccList(" + str(self.var) + "," + str(self.index) + ")"

    def eval(self):	
        return 'variables["' + self.var.var + "][" + self.index.eval() + "]"

class AccTab(Expresion):
    def __init__(self,var,col,index):
        Expresion.__init__(self)
        self.var = var
        self.col = col
        self.index = index

    def __str__(self):
        return "AccTab(" + str(self.var) + "," + self.col + "," + str(self.index) + ")"

    def eval(self):
        return 'variables["' + self.var.var + '"][' + self.index.eval() + "]." + self.col

class Tabla(Expresion):
    def __init__(self,tam,col):
        Expresion.__init__(self)
        self.tam = tam
        self.col = col

    def __str__(self):
        aux = '['
        for c in self.col:
            aux = aux + '(' + str(c.var) + ',' + str(c.type) + ',' + str(c.exp) + ')' + ','
        aux = aux[:-1] + ']'

        return "Tabla(" + str(self.tam) + "," + aux + ")"

    def eval(self):
        return ''

class ColTabla:
    def __init__(self,var,type,exp,tipo=None):
        self.var = var
        # tipo por definicion
        self.type = type
        # tipo inferido de la expresion 
        self.tipo = tipo
        self.exp = exp

    def __str__(self):
        return "ColTabla(" + str(self.var) + "," + self.type + "," + str(self.exp) + ")"

    def eval(self):
        return self.var.eval()

class Range(Expresion):
    def __init__(self,ini,fin):
        Expresion.__init__(self)
        self.ini = ini
        self.fin = fin

    def __str__(self):
        return "Range(" + str(self.ini) + "," + str(self.fin) + ")"

    def eval(self):
        aux = '[]'

        if self.ini.num < self.fin.num:
            return str(range(self.ini.num, self.fin.num + 1))

        return aux

class Len(Expresion):
    def __init__(self,var):
        Expresion.__init__(self)
        self.var = var

    def __str__(self):
        return "Len(" + str(self.var) + ")"

    def eval(self):
        return "length." + self.var.eval()

class Cuant(Expresion):
    def __init__(self,op,var,list,exp):
        Expresion.__init__(self)
        self.op = op
        self.var = var
        self.list = list
        self.exp = exp

    def __str__(self):
        return "Cuant(" + str(self.op) + "," + str(self.var) + "," + str(self.list) + "," + str(self.exp) + ")"

class List(Expresion):
    def __init__(self,list):
        Expresion.__init__(self)
        self.list =  list

    def __str__(self):
        aux = '['
        for exp in self.list:
            aux = aux + str(exp) + ','
        aux = aux[:-1] + ']'

        return "List(" + aux + ")" 

class Num(Expresion):
    def __init__(self,num):
        Expresion.__init__(self)
        self.num = num

    def __str__(self):
        return "Num("+ str(self.num) +")"

    def eval(self):
        return str(self.num)

class String(Expresion):
    def __init__(self,string):
        Expresion.__init__(self)
        self.string = string

    def __str__(self):
        return "String("+ self.string +")"

    def eval(self):
        return self.string


class Var(Expresion):
    def __init__(self,var):
        Expresion.__init__(self)
        self.var = var

    def __str__(self):
        return "Var("+ self.var + ")"

    def eval(self):
        return 'variables["' + self.var + '"]'

############################################################################
#########            PRODUCCIONES DE LA GRAMATICA                 ##########
############################################################################

def p_program_dec(p):
    '''program : EQ declaraciones
        | declaraciones'''

    # Tabla de simbolos para el tag de shiny 
    nombres={}
    error=False

    if len(p) == 3:
        p[2][2].reverse()
        aux = []
        for i,var in enumerate(p[2][0]):
            aux.append(Dec(var,p[2][1][i],p[2][2][i]))
            if isinstance(p[2][2][i],Tabla):
                col = p[2][2][i].col
                simb_tabletype = {}
                for c in col:
                    if c.var.var in simb_tabletype:
                        print "Error: variable "+c.var.var+"' declarada mas de una vez en la tabla '"+var.var+"'"
                        error=True
                    simb_tabletype[c.var.var] = (c.type,c.exp)
                nombres[var.var] = (p[2][1][i],(p[2][2][i].tam,simb_tabletype),True)    
            else:
                if var.var in nombres:
                    print "Error: variable '"+var.var+"' declarada mas de una vez"
                    error=True
                nombres[var.var] = (p[2][1][i],p[2][2][i],True)
        p[0] = (Salida(aux),nombres,error)
    else:
        p[1][2].reverse()
        aux = []
        for i,var in enumerate(p[1][0]):
            aux.append(Dec(var,p[1][1][i],p[1][2][i]))
            if isinstance(p[1][2][i],Tabla):
                col = p[1][2][i].col
                simb_tabletype = {}
                for c in col:
                    if c.var.var in simb_tabletype:
                        print "Error: variable '"+c.var.var+"' declarada mas de una vez en la tabla '"+ var.var+"'"
                        error=True
                    simb_tabletype[c.var.var] = (c.type,c.exp)
                nombres[var.var] = (p[1][1][i],(p[1][2][i].tam,simb_tabletype),False)    
            else:
                if var.var in nombres:
                    print "Error: variable '"+var.var+"' declarada mas de una vez"
                    error=True
                nombres[var.var] = (p[1][1][i],p[1][2][i],False)	
        p[0] = (NoSalida(aux),nombres,error)

def p_program_exp(p):
    'program : EQ expresion'
    error=False
    if len(p) == 3:
        p[0] = (SalidaExpresion(p[2]),{},error)

def p_empty(p):
    'empty :'
    p[0] = ''
    pass

def p_declaraciones(p):
    '''declaraciones : VAR COLON type COMMA declaraciones COMMA expresion
        | VAR COLON type ASIG expresion ''' 
    if len(p) == 6:
        p[0] = ([Var(p[1])],[p[3]],[p[5]])
    else:
        p[5][0].append(Var(p[1]))
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

def p_aux_1(p):
    'aux : VAR'
    p[0]= Var(p[1])

def p_aux_2(p):
    ''' aux : NUM
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
            p[0] = AccTab(Var(p[1]),p[6],p[3])
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
            p[0] = AccList(Var(p[1]),p[3])
    elif len(p) == 4:
        p[0] = AccTab(Var(p[1]),Var(p[3]),0)
    elif len(p) == 3:
        p[0] = Min(p[2])
    elif isinstance(p[1],int):
        p[0]= Num(p[1])
    elif isinstance(p[1],str):
        p[0]= String(p[1])
    else:
        p[0] = p[1]

def p_m(p):
    ''' m : MINUS %prec UMINUS
        | NOT %prec UNOT
        | empty'''
    p[0] = p[1]

def p_cuant(p):
    'cuant : LLIST cuan VAR COLON operando COLON operando RLIST'
    p[0] = Cuant(p[2],Var(p[3]),p[5],p[7])

def p_list(p):
    '''list : LLIST VAR COLON operando COLON operando RLIST
        | LBRACK expList RBRACK'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = Cuant('',Var(p[2]),p[4],p[6])

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
        p[1].list.append(Var(p[3]))
        p[0] = p[1]
    else:
        p[0] = List([Var(p[1])])

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
    'tabla : NEW TABLE LBRACK NUM RBRACK WHERE col'
    p[0] = Tabla(p[4],p[7])

def p_col(p):
    ''' col : VAR COLON typ ASIG expresion
        | col SEMICOLON VAR COLON typ ASIG expresion'''
    if len(p) == 8:
        p[1].append(ColTabla(Var(p[3]),p[5],p[7]))
        p[0] = p[1]
    else:
        p[0] = [ColTabla(Var(p[1]),p[3],p[5])]

def p_typ(p):
    '''typ : INT
        | TSTRING'''
    p[0] = p[1]

def p_error(p):
    print "Error de sintaxis: %r" % p.value
