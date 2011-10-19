def extraerArgumentos(argumentos):
	palabras = []
	archivos = []
	i = 1
	for a in argumentos[1:]:
		if(a[0] == '+' or a[0] == '-'):
			palabras.append(a[1:])
			i = i +1
	archivos = argumentos[i:]
	return (palabras,archivos)