# --------------------------------------------------------------------------
# Programa que tiene como entrada un archivo html,con tags de codigo shinyEL.
# Realiza el analisis lexicografico y sintactico de los fragmentos shinyEL. 
#
# Devuelve una representacion intermedia del codigo html con marcas en donde 
# aparecen los tags de shinyEL. Y construye el grafo de dependencias. 
#
# Autores : Hancel Gonzalez   07-40983
#           Jennifer Dos Reis 08-10323
#
# -------------------------------------------------------------------------

import lexer_parser
import ply.lex as lex
import ply.yacc as yacc
import sys

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
		
### Crear grafo de dependencias
##for table in tables:
##    for var in keys(table):
##        if tabla[var][0]=="table":
##            for varT in keys(tabla[var][1]):
##                recorrer(var+ "." + varT,tabla[var][1][varT][1])
##        else:
##            recorrer(var,table[var][1])

##def recorrer(var,expr):
##    if issubclass(expr,BinOp):
##        # recorrer para cada hijo
##    elif issubclass(expr,UnOp):
##        # recorrer para un hijo
##    elif isinstance(expr,IfExp):
##        # se debe recorrer cond para ver si cambia
##        # los otros dos hijos importan?
##    elif isinstance(expr,AccList):
##        # Esto es var[index] ? recorrer index y
##        # como hago para saber si cambia var[index] ??
##    elif isinstance(expr,AccTab):
##        # var.var[index]
##        # recorrer index
##        # Como hago con var[index] y var.var[index]
##    elif isinstance(expr,Range):
##        # recorrer expr.ini y expr.fin
##    elif isinstance(expr,Len):
##        # recorrer expr.var
##    elif isinstance(expr,List):
##        # para cada elemento de self.list recorrer
