import sys
import funciones

  
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

(dic_permitidas,list_prohibidas) =funciones.procesarPalabras(palabras)

files = funciones.procesarArchivos(archivos)
