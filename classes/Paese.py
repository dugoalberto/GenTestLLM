class Paese:
    def __init__(self, nome, fuso):
        self.nome = nome
        self.fuso = fuso
    def get_nome(self):
        return self.nome
    def get_fuso(self):
        return self.fuso
    def set_nome(self, nome):
        self.nome = nome
        return self.nome
    def set_fuso(self, fuso):
        self.fuso = fuso
        return self.fuso
    def get_paese(self):
        return self.nome, self.fuso
    def set_paese(self, nome, fuso):
        self.nome = nome
        self.fuso = fuso
        return self.nome, self.fuso
    def __str__(self):
        return self.nome + " " + str(self.fuso)
    def __eq__(self, other):
        return self.nome == other.nome and self.fuso == other.fuso
    def equals(self, other):
        return self.__eq__(other)
    def semiquals(self):
        return self.nome == "Italia"

