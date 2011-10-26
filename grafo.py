# Definicion de la Clase Digrafo y sus metodos
class Digrafo:
    # Metodo que se ejecuta justo despues que se crea el objeto
    def __init__(self):
        self.arcos_in = {}
        self.arcos_out = {}
        self.nodos = -1

    # Anade nodo al grafo
    def anadirNodo(self):
        self.nodos = self.nodos + 1
        nodo = self.nodos

        if nodo not in self.arcos_in:
            self.arcos_in[nodo] = []

        if nodo not in self.arcos_out:
            self.arcos_out[nodo] = []

        return nodo
    
    # Remueve un nodo del grafo, consigo se eliminan
    # los arcos adyacentes y subyacentes
    def removerNodo(self,nodo):
        for node in self.arcos_in.keys():
            if(node != nodo):
                for aux in self.arcos_in[node]:
                    if(aux[0] == nodo):
                        self.arcos_in[node].remove(aux)
                for aux in self.arcos_out[node]:
                    if(aux[0] == nodo):
                        self.arcos_out[node].remove(aux)

        del self.arcos_in[nodo]
        del self.arcos_out[nodo]

    # Anade un arco con etiqueta al grafo
    def anadirArco(self,src,dst,exp):
        if(src in self.arcos_in and src in self.arcos_out and
           dst in self.arcos_in and dst in self.arcos_out):
            self.arcos_in[src].append((dst,exp))
            self.arcos_out[dst].append((src,exp))

    # Remueve un arco del grafo        
    def removerArco(self,src,dst):
        for aux in self.arcos_in[src]:
            if(aux[0] == dst):
                self.arcos_in[src].remove(aux)
                break

        for aux in self.arcos_out[dst]:
            if(aux[0] == src):
                self.arcos_out[dst].remove(aux)
                break

    # Verifica si en uno nodo hay un bucle, de ser asi
    # retorna el arco etiquetado correspondiente
    def isBucle(self,node):
        in_ = self.arcos_out[node]
        for nodo, expr in in_:
            if(nodo == node):
                return (nodo,expr)
        return False

    # Verifica la existencia de una arco, de ser cierto
    # retorna el arco etiquetado correspondiente
    def isArco(self,src,dst):
        for dst_, expr in self.arcos_in[src]:
            if(dst_ == dst):
                return (dst_,expr)
        return False
    
    # Dado un nodo y una expr, se busca el nodo destino
    # correspondiente 
    def nodoDestino(self,src,expr):
        for dst in self.arcos_in[src]:
            if(dst[1] == expr):
                return dst[0]

    # Retorna la expresion regular asociada al DFA (en caso 
    # de que el grafo sea tratado como tal)
    def convertirDFA_ER(self):
        #Crear estados 'i' y 'f'
        self.arcos_in['i'] = []
        self.arcos_out['i'] = []
        self.arcos_in['f'] = []
        self.arcos_out['f'] = []
        #Conectar estado inicial 'i' con el estado 0
        self.anadirArco('i',0,'')
        #Conectar estados finales anteriores con el estado final 'f'
        for f in range(self.nodos + 1):
            self.anadirArco(f,'f','')
        #Eliminacion de arcos
        for q in range(self.nodos + 1):
            #Verificacion de bucle en el nodo q
            star = self.isBucle(q)
            #Si es asi, se obtiene la expresion regular de cero o mas repeticiones
            if(star):
                self.arcos_out[q].remove(star)
                self.arcos_in[q].remove(star)
                star = '(?:' + star[1] + ')*'
            else:
                star = ''
            # Se crean arcos que se conectaban con el estado q
            in_ = self.arcos_out[q]
            out_ = self.arcos_in[q]
            for i,expr1 in in_:
                for o, expr2 in out_:
                    er = expr1 + star + expr2
                    arc = self.isArco(i,o)
                    if(arc):
                        # Si existe el arco, existe una expresion regular asociada
                        self.removerArco(i,o)
                        er = '(?:' + arc[1] + ')|(?:' + er + ')'
                        self.anadirArco(i,o,er)
                    else:
                        # Como el arco no existe, se crea uno nuevo
                        er = '(?:' + er + ')'
                        self.anadirArco(i,o,er)
            self.removerNodo(q)
        return self.arcos_in['i'][0][1]
