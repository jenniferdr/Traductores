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

class		