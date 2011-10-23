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

(dic_permitidas,list_prohibidas) =funciones.procesarPalabras(palabras)

# Con todas sus permutaciones de palabras en diccionario 
#ER=..NP palabra NP palabra.. 
## compilarla

#for file in files:
#    for line in file:
#        if(re.search("^"+ER+"$",line):
#           print line

# Y finnn :)
