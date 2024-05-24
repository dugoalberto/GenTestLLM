

class Ufficio:
    def __init__(self, indirizzo, metratura, scrivanie):
        self.indirizzo = indirizzo
        self.metratura = metratura #in metri quadrati
        self.scrivanie = scrivanie #lista di scrivanie
    def massimo_scrivanie(self):
        area = 0
        for s in self.scrivanie:
            area += s.get_area()
            print(area)
        if area == 0:
            return 0
        return int(self.metratura / area)
    def qt_scrivanie(self):
        return len(self.scrivanie)
    def get_indirizzo(self):
        return self.indirizzo
    def get_metratura(self):
        return self.metratura
    def get_scrivanie(self):
        return self.scrivanie
    def set_indirizzo(self, indirizzo):
        self.indirizzo = indirizzo
        return self.indirizzo
    def set_metratura(self, metratura):
        self.metratura = metratura
        return self.metratura
    def set_scrivanie(self, scrivanie):
        self.scrivanie = scrivanie
        return self.scrivanie

