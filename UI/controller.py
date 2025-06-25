import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._album = None
        self._durata = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        try:
            self._durata = int(self._view._txtInDurata.value)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Inserire un valore intero per i minuti."))
            self._view.update_page()
            return
        self._model.buildGraph(self._durata)
        nodi, archi = self._model.getInfoGraph()
        self._view.txt_result.controls.append(ft.Text(f"Nodi: {nodi}, archi: {archi}"))
        for album in self._model.getEdges():
            self._view._ddAlbum.options.append(ft.dropdown.Option(key=album.title, data=album, on_click=self.pickAlbum))
        self._view.update_page()

    def pickAlbum(self, e):
        self._album = e.control.data

    def getSelectedAlbum(self, e):
        pass

    def handleAnalisiComp(self, e):
        self._view._ddAlbum.options.clear()
        if self._model.existGraph() or self._album is None:
            self._view.txt_result.controls.append(ft.Text("Creare prima il grafo e selezionare un album."))
            self._view.update_page()
            return
        c, l = self._model.handleAlbum(self._album)
        self._view.txt_result.controls.append(ft.Text(f"Dimensione: {c}, Durata totale: {l}"))
        self._view.update_page()

    def handleGetSetAlbum(self, e):
        try:
            tot = int(self._view._txtInSoglia.value)
        except:
            tot = None
        print(self._model.existGraph(), self._album, tot)
        if self._model.existGraph() or self._album is None or tot is None:
            self._view.txt_result.controls.append(ft.Text("Creare prima il grafo, selezionare un album e inserire una durata."))
            self._view.update_page()
            return
        percorso = self._model.getPercorso(self._album, tot)
        for p in percorso:
            self._view.txt_result.controls.append(ft.Text(p))
        self._view.update_page()