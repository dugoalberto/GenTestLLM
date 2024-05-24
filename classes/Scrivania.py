class Scrivania:
    def __init__(self, larghezza, altezza, profondita):
        self.larghezza = larghezza/100
        self.altezza = altezza/100
        self.profondita = profondita/100
    def get_larghezza(self):
        return self.larghezza
    def get_altezza(self):
        return self.altezza
    def get_profondita(self):
        return self.profondita
    def get_dimensioni(self):
        return self.larghezza, self.altezza, self.profondita
    def set_larghezza(self, larghezza):
        self.larghezza = larghezza/100
        return self.larghezza
    def set_altezza(self, altezza):
        self.altezza = altezza/100
        return self.altezza
    def set_profondita(self, profondita):
        self.profondita = profondita/100
        return self.profondita
    def set_dimensioni(self, larghezza, altezza, profondita):
        self.larghezza = larghezza/100
        self.altezza = altezza/100
        self.profondita = profondita/100
        return self.larghezza, self.altezza, self.profondita
    def get_volume(self):
        return self.larghezza * self.altezza * self.profondita
    def get_area(self):
        return self.larghezza * self.altezza
