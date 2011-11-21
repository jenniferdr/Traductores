# --------------------------------------------------
# Reconocedor de codigo ShinyEl.
# 
# Autores : Hancel Gonzalez   07-40983
#           Jennifer Dos Reis 08-10323
#
# --------------------------------------------------

import lexer_parser
import ply.lex as lex
import ply.yacc as yacc
import sys

lexer = lex.lex(module=lexer_parser)
parser = yacc.yacc(module=lexer_parser,start='program',errorlog=yacc.NullLogger())

data = sys.argv[1]

file = open(data,"r")

while True:
    b = ''
    bl = False
    s1 = file.read(1)
    if len(s1) == 0 :
        break    
    if s1 == '{':
        s1 = file.read(1)
        while True:
            s1 = file.read(1)
            if s1 == '%':
                s1 = file.read(1)
                if  s1 == '}':
                    bl = True
                    break
                else:
                    b = b + s1
            else:
                b = b + s1
    if bl:
        print "\n" + b
        lexer.input(b)
        for tok in lexer: print tok
        result = parser.parse(b)
        print result
