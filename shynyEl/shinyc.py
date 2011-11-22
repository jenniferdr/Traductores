# --------------------------------------------------------------------------
# Programa que tiene como entrada un archivo html con tags de codigo shinyEL.
# Realiza el analisis lexicografico y sintactico de los fragmentos shinyEL. 
#
# Devuelve una representacion intermedia del codigo html con marcas en donde 
# aparecen los tags de shinyEL. Y construye el grafo de dependencias. 
#
# Version 0.1
#
# Autores : Hancel Gonzalez   07-40983
#           Jennifer Dos Reis 08-10323
#
# -------------------------------------------------------------------------

import lexer_parser
import ply.lex as lex
import ply.yacc as yacc
import networkx as nx
import matplotlib.pyplot as plt
import sys

# Funcion que recibe el nombre de una variable var y una expresion expr.
# Va anadiendo arcos que van desde las variables que se encuentran dentro
# de la expresion expr hasta la variable var en el grafo declarado como
# variable global GD (Grafo de dependencias). 
def recorrer(var,expr):
    
    if isinstance(expr,lexer_parser.BinOp):
        # op1 opBinnario op2
        recorrer(var,expr.op1)
        recorrer(var,expr.op2)
    elif isinstance(expr,lexer_parser.UnOp):
        # opUnario(op)
        recorrer(var,expr.op)
    elif isinstance(expr,lexer_parser.IfExp):
        # Expresion IF cond THEN expr1 ELSE expr2 
        # Como sabemos de cual expresion depende? 
        recorrer(var,expr.cond)
        recorrer(var,expr.exp1)
        recorrer(var,expr.exp2)
    elif isinstance(expr,lexer_parser.AccList):
        # Acceso a lista: var[index]
        # Como sabemos que si se cambia un elemento cualquiera 
        # de la lista var por otro lado, afecta a esta expresion?
        recorrer(var,expr.index)
        recorrer(var,expr.var)
    elif isinstance(expr,lexer_parser.AccTab):
        # Acceso a tabla: var[index].var
        recorrer(var,expr.index)
        # Como hago con var[i].var, saber cuanto es i
        # para poder agregarlo al grafo.? 
    elif isinstance(expr,lexer_parser.Range):
        # Funcion range(ini,fin)
        recorrer(var,expr.ini)
        recorrer(var,expr.fin)
    elif isinstance(expr,lexer_parser.Len):
        # Funcion Len(var)
        recorrer(var,expr.var)
    elif isinstance(expr,lexer_parser.List):
        # Recorrer cada elemento de la lista
        for elem in (expr.list):
            recorrer(var,elem)
    elif isinstance(expr,lexer_parser.Var):
        # Caso base: expr es una variable
        GD.add_edge(var,expr.var)

#################################################################################
        

lexer = lex.lex(module=lexer_parser)
parser = yacc.yacc(module=lexer_parser,start='program',errorlog=yacc.NullLogger())

data = sys.argv[1]

file = open(data,"r")

salida = "marcas_" + file.name

file_e = open(salida,"w")

tables = []
i = 1
while True:
    b = ''
    bl = False
    s1 = file.read(1)
    if len(s1) == 0 :
        break    
    if s1 == '{':
        s1 = file.read(1)
        file_e.write("marca_shiny_"+str(i))
        while True:
            s1 = file.read(1)
            if s1 == '%':
                s2 = file.read(1)
                if  s2 == '}':
                    bl = True
                    i += 1
                    break
                else:
                    b = b + s1 + s2
            else:
                b = b + s1
    else:
        file_e.write(s1)
        
    if bl:
        print "\n" + b
        lexer.input(b)
        #for tok in lexer: print tok
        result = parser.parse(b)
        tables.append(result[1])
        print result[1]

file_e.close()
		
# Crear grafo de dependencias
global GD
GD= nx.DiGraph()

for table in tables:
    for var in table.keys():
        if table[var][0]=="table":
            for varT in table[var][1].keys():
                recorrer(var+ "." + varT,table[var][1][varT][1])
        else:
            recorrer(var,table[var][1])

nx.draw(GD)
plt.show()


