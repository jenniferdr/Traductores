import sys
import funciones
  
if('-' in sys.argv):
	sys.argv.remove('-')

if(len(sys.argv) < 3):
	print "Faltan parametros"
	sys.exit(0)
elif((len(sys.argv) == 3) and ((sys.argv[1][0] != '+' and sys.argv[1][0] != '-')
			       or sys.argv[2][0] == '+' or sys.argv[2][0] == '-')):
	print "Parametros invalidos"
	sys.exit(0) 
    
(palabras,archivos) = funciones.extraerArgumentos(sys.argv)

if((len(palabras) == 0) or (len(archivos) == 0)):
	print ("Faltan parametros: debe haber por lo menos una palabra y"
	       " un archivo")
	sys.exit(0)
    
files = funciones.procesarArchivos(archivos)    

global dic_permitidas # Palabras permitidas con el numero de veces que deben aparecer
global list_prohibidas # Lista de palabras que no deben aparecer o aparecen un numero exacto de veces 

(dic_permitidas,list_prohibidas) =funciones.procesarPalabras(palabras)

listaLP = funciones.listaLetras(list_prohibidas) # Lista de letras pertenecientes a las palabras prohibidas

# dfa = new Graph()
# dfa = funciones.dfaPalabras(listaLP) # DFA formado con las letras de las palabras prohibidas

# palabras_LP=funciones.convertirA_ER(dfa) # Expresion regular de palabras formadas con las letras de palabras prohibidas.

# ER para representar cualquier caracter menos las que aparecen
# en las palabras prohibidas
#strLNP="[^"
#for l in listaLP:
#    strLP += l
#str += "]"

# ER para representar cualquier palabra menos las prohibidas     
#NP= "("+strLNP+"*("+palabras_LP+strLNP+"+|"+strLNP+")*"+palabras_LP+"?)" 

# Con todas sus permutaciones de palabras en diccionario 
#ER=..NP palabra NP palabra.. 
## compilarla

#for file in files:
#    for line in file:
#        if(re.match("^"+ER+"$",line):
#           print line

# Y finnn :)
