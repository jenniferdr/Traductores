import sys
import funciones

if('-' in argv)
	argv.remove('-')

if(len(sys.argv) < 3):
	print "Faltan parametros"
	exit
elif((len(sys.argv) == 3) and (argv[1] != '+' or argv[1] != '-') and
     (argv[2] == '+' or argv[2] == '-')):
	print "Parametros invalidos"
	exit

(palabras,archivos) = extraerArgumentos(argv)

if(len(palabras) == 0 or len(archivos) == 0)
	print ("Faltan parametros: debe haber por lo menos una palabra y"
	       "un archivo")

(dic_permitidas,list_prohibidas) = procesarPalabras(palabras)

files = procesarArchivos(archivos)