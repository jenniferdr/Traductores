class Digrafo:
    def __init__(self):
        self.arcos_in = {}
        self.arcos_out = {}
        self.nodos = -1

    def anadirNodo(self):
        self.nodos = self.nodos + 1
        nodo = self.nodos

        if nodo not in self.arcos_in:
            self.arcos_in[nodo] = []

        if nodo not in self.arcos_out:
            self.arcos_out[nodo] = []

        return nodo

    def anadirArco(self,src,dst,exp):
        if(src in self.arcos_in and src in self.arcos_out and
           dst in self.arcos_in and dst in self.arcos_out):
            self.arcos_in[src].append((dst,exp))
            self.arcos_out[dst].append((src,exp))

    def dfa2er(dfa):
