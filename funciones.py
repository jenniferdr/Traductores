def extraerArgumentos(argumentos):
	palabras = []
	archivos = []
	i = 1
	for a in argumentos[1:]:
		if(a[0] == '+' or a[0] == '-'):
			palabras.append(a)
			i = i +1
	archivos = argumentos[i:]
	return (palabras,archivos)
	
def procesarPalabras(palabras):
	permitidas = {}
	prohibidas = []
	for p in palabras:
		if(p[0] == '+'):
			if(p[1:] in permitidas):
				permitidas[p[1:]] = permitidas[p[1:]] + 1
			else:
				permitidas[p[1:]] = 1
		elif(p[0] == '-' and not(p[1:] in prohibidas)):
			prohibidas.append(p[1:])
	return (permitidas,prohibidas)
	
def procesarArchivos(archivos):
	pointer_files = []
	for f in archivos:
		try:
			pointer_files.add(open(f, "r"))		
		except:
			print "Error al abrir el archivo '" + f + "'"
	return pointer_files

def listaLetras(palabras):
    letras=[]
    for p in palabras:
        for l in p:
            if(not(l in letras)):
                letras.append(l)
    return letras

            
def dfaPalabras(listaLetras):
    global G=grafo.Graph()
    G.addNodo()
    global listaL
    listaL= listaLetras
    global primeras
    primeras=[]
    
    #Tomar la primera letra de cada palabra
    for palabra in list_prohibidas:
	    if(!(palabra[0] in primeras)):
		    primeras.append(palabra[0])

    #Si alguna palabra prohibida es de long 1 esa letra se debe eliminar
    # del conjunto de letras a utilizar en el automata
    for palabra in list_prohibidas:
	    if(len(palabra)==1): 
		    listaL.remove(palabra[0])
		    primeras.remove(palabra[0])
    global i
    i=1
    #Crear un nodo y un arco para la primera letra de cada palabra prohibida
    for letra in primeras:
            G.addNodo()
            G.addArc(0,i,letra)
            i= i+1

    # Hacer un bucle en el estado inicial con las letras no iniciales 
    for l in listaL:
        if(not(l is in primeras)):
            G.addArc(0,0,l)

    # Hacer un diccionario que dada una letra tenga la lista de palabras 
    # que comience por esa letra
    

    i=1        
    # Para cada nodo creado, calcular el resto de los caminos 
    for l in primeras:
        #Tomar las palabras que comienzan por la letra l 
	dfaAux()
    
    
