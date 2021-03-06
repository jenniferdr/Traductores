import sys
import funciones
import grafo

if('-' in sys.argv):
	sys.argv.remove('-')

if(len(sys.argv) < 3):
	print "Faltan parametros"
	exit
elif((len(sys.argv) == 3) and ((sys.argv[1][0] != '+' and sys.argv[1][0] != '-')
			       or sys.argv[2][0] == '+' or sys.argv[2][0] == '-')):
	print "Parametros invalidos"
	exit
    
(palabras,archivos) = funciones.extraerArgumentos(sys.argv)

if((len(palabras) == 0) or (len(archivos) == 0)):
	print ("Faltan parametros: debe haber por lo menos una palabra y"
	       "un archivo")
    
files = funciones.procesarArchivos(archivos)    

# Obtener un diccionario de palabras permitidas y lista de prohibidas
(dic_permitidas,list_prohibidas) =funciones.procesarPalabras(palabras)

# Lista de letras pertenecientes a las palabras prohibidas
listaLP= funciones.listaLetras(list_prohibidas)

## dfa= new Graph()
# DFA formado con las letras de las palabras prohibidas
dfa= funciones.dfaPalabras(listaLP,list_prohibidas)

# Expresion regular de palabras formadas con las letras
# de palabras prohibidas. 
palabras_LP=dfa.convertirDFA_ER()

# ER para representar cualquier caracter menos las que aparecen
# en las palabras prohibidas
strLNP="[^"
for l in listaLP:
    strLNP += l
strLNP += "]"

# ER para representar cualquier palabra menos las prohibidas     
NP= "("+strLNP+"*("+palabras_LP+strLNP+"+|"+strLNP+")*"+palabras_LP+"?)" 
print NP
# Con todas sus permutaciones de palabras en diccionario 
#ER=..NP palabra NP palabra.. 
## compilarla

#for file in files:
#    for line in file:
#        if(re.match("^"+ER+"$",line):
#           print line

# Y finnn :) 

           

