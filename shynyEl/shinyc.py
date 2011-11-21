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

data = "a:int := c + v"

lexer = lex.lex(module=lexer_parser)

lexer.input(data)

for tok in lexer:
    print tok

parser = yacc.yacc(module=lexer_parser,start='program',errorlog=yacc.NullLogger())

result = parser.parse(data)

print result