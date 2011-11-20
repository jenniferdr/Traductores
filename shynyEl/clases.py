class Expresion: pass

class BinOp(Expresion):
    def __init__(self,op1,op2):
        self.op1 = op1
        self.op2 = op2

class UnOp(Expresion):
    def __init__(self,opd,op):
        self.opd = opd	
        self.op = op

class Ctte(Expresion):
    def __init__(self,valor)
	    self.valor = valor

class TbyOp(Expresion):
    def __init__(self,exp,vars):
        self.exp = exp
        self.vars = vars

class IfExp(Expresion):
    def __init__(self,cond,exp1,exp2):
        self.cond = cond
        self.exp1 = exp1
        self.exp2 = exp2

class Dec:
    def __init__(self,var,type,exp):
        self.var = var
        self.type = type
        self.exp = exp

class AccList(Expresion):
    def __init__(self,var,index):
        self.var = var
        self.index = index

class AccTab(Expresion):
    def __init___(self,var,col,index):
        self.var = var
        self.col = col
        self.index = index

class Salida:
    def __init___(self,exp):
        self.exp = exp
		
class Tabla(Expresion):
    def __init__(self,name,tam,col):
        self.name = name
        self.tam = tam
        self.col = col

class ColTabla:
    def __init__(self,var,type,exp):
        self.var = var
		self.type = type
		self.exp = exp
		
class Range(Expresion):
    def __init__(self,ini,fin):
        self.ini = ini
        self.fin = fin

class Len(Expresion):
    def __init__(self,var):
        self.var = var
		
class Program:
    def __init__(self,exp):
        self.exp = exp
		
class Cuant(Expresion):
    def __init__(self,op,var,list,exp):
        self.op = op
        self.var = var
        self.list = list
        self.exp = exp		