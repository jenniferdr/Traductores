import grafo
import sys
    
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
			pointer_files.append(open(f, "r"))		
		except:
			print "Error al abrir el archivo '" + f + "'"
			if(len(archivos) == 1):
				sys.exit(0)
	return pointer_files

    
def listaLetras(palabras):
    letras=[]
    for p in palabras:
        for l in p:
            if(not(l in letras)):
                letras.append(l)
    return letras

            
def dfaPalabras(listaLetras,prohibidas):
    global G
    G=grafo.Digrafo()
    G.anadirNodo()
    global listaL
    listaL= listaLetras
    global primeras
    primeras=[]
    global list_prohibidas
    list_prohibidas=prohibidas
    
    #Tomar la primera letra de cada palabra
    for palabra in list_prohibidas:
	    if(not(palabra[0] in primeras)):
		    primeras.append(palabra[0])

    #Si alguna palabra prohibida es de long 1 esa letra se debe eliminar
    # del conjunto de letras a utilizar en el automata
    for palabra in list_prohibidas:
	    if(len(palabra)==1): 
		    listaL.remove(palabra[0])
		    primeras.remove(palabra[0])
            
    #Crear un nodo y un arco para la primera letra de cada palabra prohibida
    for letra in primeras:
            i=G.anadirNodo()
            G.anadirArco(0,i,letra)

    # Hacer un bucle en el estado inicial con las letras no iniciales
    noIniciales="("
    for l in listaL:
        if(not(l in primeras)):
            noIniciales+= (l+"|")
            
    noIniciales= noIniciales[:-1] + ")"
    G.anadirArco(0,0,noIniciales)
            
    noDelegables=[]  

    i=0
    # Para cada nodo creado, calcular el resto de los caminos 
    for l in primeras:
        nuevasPalabras=[]
        for palabra in list_prohibidas:
            if(palabra[0]==l):
                nuevasPalabras.append(palabra[1:])
                noDelegables.append(palabra[1])
            else:
                nuevasPalabras.append(palabra)
        i= i+1        
        dfaAux(nuevasPalabras,i,noDelegables)
    return G



def dfaAux(palabras,nodoActual,noDelegables):
    nuevos=[]
    delegar=[]
    # Clasificar letras en delegables a otros estados o nuevos estados
    for letra in listaL:
        p=False
        termina= False
        
        for palabra in palabras:
            if(len(palabra)==1): termina=True
            if(palabra[0]==letra):
                p=True
                if(letra in noDelegables):
                    if(not(letra in nuevos)): nuevos.append(letra)
                else:
                    if(not(letra in delegar)): delegar.append(letra)
        if(not(p)):
            if(not(letra in delegar)): delegar.append(letra)
        if(termina):
            if(letra in nuevos): nuevos.remove(letra)
            if(letra in delegar): delegar.remove(letra)
    sucesores={}
    # Crear los nuevos nodos o estados
    for letra in nuevos[:]:
        i= G.anadirNodo()
        G.anadirArco(nodoActual,i,letra)
        sucesores[i]= letra
        nuevos.remove(letra)

    # Delegar letras a otros estados
    # Primero formamos la expresion regular de todas las letras que van
    # al estado inicial
    aEdoIni="("
    for letra in delegar[:]:
        if(not(letra in primeras)): delegar.remove(letra)
        aEdoIni+= letra + "|"
        
    aEdoIni= aEdoIni[:-1] + ")"
    # Agragar el arco al estado inicial
    if(len(aEdoIni)>1):
        G.anadirArco(nodoActual,0,aEdoIni)

    # Luego delegamos las letras que van a los estados que no es el inicial
    for letra in delegar[:]:
        nodoDest=G.nodoDestino(0,delegar.pop())
        G.anadirArco(nodoActual,nodoDest,letra)

    # Pila de nuevos,delegar y noDelegables vaciadas 
    noDelegables=[]

    # Para cada nodo sucesor, calcular el resto de los caminos 
    for nodo in sucesores.keys():
        letra= sucesores[nodo]
        nuevasPalabras=[]
        i=0
        for palabra in palabras:
            if(palabra[0]==letra):
                nuevasPalabras.append(palabra[1:])
                noDelegables.append(palabra[1])
            else:
                nuevasPalabras.append(list_prohibidas[i])
        i= i+1        
        dfaAux(nuevasPalabras,nodo,noDelegables)
    
        
    
        
        
            



