import itertools
import grafo
import sys

# Funcion procesa los argumentos recibidos por la linea de comandos
# Recibe una lista de argumentos
# Retorna una tupla con dos listas: las reglas y los archivos    
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

# Funcion que procesa la lista de reglas recibidas como argumentos
# Recibe una lista de palabras las cuales comienzan por + o -
# Retorna una tupla la cual contiene:
#  - Un diccionario cuya claves son las palabras permitidas y valor 
#    numero de repeticiones 
#  - Una lista de palabras prohibidas
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
	
# Funcion que procesa los archivos aportados en los argumentos
# Recibe una lista con los nombres de los archivos
# Retorna una lista de objetos del tipo file para cada archivo
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

# Funcion que procesa las palabras de una lista
# Recibe una lista de palabras 
# Retorna una lista con las letras que conforman las palabras
# recibidas, sin repeticiones
def listaLetras(palabras):
    letras=[]
    for p in palabras:
        for l in p:
            if(not(l in letras)):
                letras.append(l)
    return letras

# Funcion que retorna un automata deterministico dadas una lista 
# de letras y una de palabras
# Retorna un DFA cuyos estados finales aceptan palabras exceptuando
# aquellas que pertenecen a la lista de palabras 'prohibidas'
def dfaPalabras(listaLetras,prohibidas,strLNP):
    global G
    G=grafo.Digrafo()
    G.anadirNodo()
    global listaL
    listaL= listaLetras[:]
    global primeras
    primeras=[]
    global list_prohibidas
    list_prohibidas=prohibidas

    print "Letras no permitidas: "+strLNP
    print "Conjunto de letras prohib: "
    print listaL
    
    #Tomar la primera letra de cada palabra
    for palabra in list_prohibidas:
	    if(not(palabra[0] in primeras)):
		    primeras.append(palabra[0])
            
    print "Las primeras letras"
    print primeras
    
    #Si alguna palabra prohibida es de long 1 esa letra se debe eliminar
    # del conjunto de letras a utilizar en el automata
    for palabra in list_prohibidas:
	    if(len(palabra)==1): 
		    listaL.remove(palabra[0])
		    primeras.remove(palabra[0])

    print "Nuevo conjunto de letras y primeras"
    print listaL
        
    #Crear un nodo y un arco para la primera letra de cada palabra prohibida
    for letra in primeras:
            i=G.anadirNodo()
            G.anadirArco(0,i,letra)
            print "Se hizo un arco del inicial letra "+letra+" nodo "
            print i
    print primeras
    # Hacer un bucle en el estado inicial con las letras no iniciales
    noIniciales="(?:"
    if(len(listaL)>0):
        for l in listaL:
            if(not(l in primeras)):
                noIniciales += l+'|'

    noIniciales += strLNP+")"
    G.anadirArco(0,0,noIniciales)
    print "bucle en el inicial con: "
    print noIniciales
        
    noDelegables=[]  

    i=0
    # Para cada nodo creado, calcular el resto de los caminos 
    for l in primeras:
        nuevasPalabras=[]
        for palabra in list_prohibidas:
            if(palabra[0]==l):
                print "La letra "+l+" es igual a "+palabra[0]
                nuevasPalabras.append(palabra[1:])
                noDelegables.append(palabra[1])
            else:
                nuevasPalabras.append(palabra)
        i= i+1        
        dfaAux(nuevasPalabras,i,noDelegables,strLNP)
    return G


# Funcion auxiliar usada por dfaPalabras
# Contruye el resto de los caminos del DFA, partiendo de ciertos nodos
def dfaAux(palabras,nodoActual,noDelegables,strLNP):
    nuevos=[]
    delegar=[]
    print "Soy el nodo"
    print nodoActual
    print "No puedo formar las palabras"
    print palabras
    
    # Clasificar letras en delegables a otros estados o nuevos estados
    for letra in listaL:
        p=False
        termina= False
        
        for palabra in palabras:
            if(palabra[0]==letra):
                if(len(palabra)==1): termina=True
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
    print "delegar y nuevos"
    print delegar
    print nuevos
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
    aEdoIni="(?:"
    for letra in delegar[:]:
        if(not(letra in primeras)):
            delegar.remove(letra)
            aEdoIni+= letra + "|"
        
    aEdoIni += strLNP+")"
    # Agregar el arco al estado inicial
    G.anadirArco(nodoActual,0,aEdoIni)
    print "estoy enviando el arco"+ aEdoIni +" al inicial "

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
        dfaAux(nuevasPalabras,nodo,noDelegables,strLNP)

# Funcion que construye una expresion regular
# Recibe una lista de palabras y un expresion regular
# Retorna la expresion regular compuesta por cada palabra 
# de la lista 'palabras', tomadas como una expresion regular,
# y la expresion regular 'er'
def crearER(palabras,er):
	palabras_=[]
	for p in palabras:
		for i in range(palabras[p]):
			palabras_.append(p)

	_palabras = itertools.permutations(palabras_)
	ER = ''
	for l in _palabras:
		aux = '(?:' + er
		for p in l:
			aux = aux + p + er
		aux = aux + ')'
		ER = ER + aux + '|'
	return ER[:len(ER)-1]
