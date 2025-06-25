import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._percorso = None
        self._nmax = 1
        self._componenteConnessa = None
        self._graph = None
        self._idNodes = dict()
        self._edges = []

    def buildGraph(self, durata):
        self._graph = nx.Graph()
        nodes = DAO.getNodes(durata)
        for node in nodes:
            self._idNodes[node.albumId] = node
        self._graph.add_nodes_from(nodes)
        self._edges = DAO.getEdges(durata, self._idNodes)
        for edge in self._edges:
            self._graph.add_edge(edge.n1, edge.n2)

    def getInfoGraph(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def existGraph(self):
        if self._graph is None:
            return True
        return False

    def getEdges(self):
        return self._idNodes.values()

    def handleAlbum(self, nodo):
        for cc in nx.connected_components(self._graph):
            if nodo in cc:
                self._componenteConnessa = cc
                lung = 0
                for album in cc:
                    lung += DAO.getDurata(album)
                return len(cc), lung

    def getPercorso(self, nodo, dtot):
        self.handleAlbum(nodo)
        rimanenti = set(self._componenteConnessa)
        rimanenti.remove(nodo)
        self.ricorsione([nodo], rimanenti, dtot)
        print(self._percorso)
        return self._percorso

    def ricorsione(self, parziale, rimanenti, dtot):
        if len(parziale) > self._nmax:
            self._nmax = len(parziale)
            self._percorso = copy.deepcopy(parziale)
        else:
            for nodo in rimanenti:
                if self.condizione(parziale, nodo, dtot):
                    parziale.append(nodo)
                    rimanenti.remove(nodo)
                    self.ricorsione(parziale, rimanenti, dtot)
                    rimanenti.add(nodo)
                    parziale.pop()

    def condizione(self, parziale, nodo, dtot):
        d = DAO.getDurata(nodo)
        for n in parziale:
            d += DAO.getDurata(n)
        if d < dtot:
            return True
        return False