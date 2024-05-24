class ContoCorrente():
    def __init__(self, nome, cognome, saldo):
        self.nome = nome
        self.cognome = cognome
        self.saldo = saldo
    def get_saldo(self):
        return self.saldo
    def set_saldo(self, saldo):
        self.saldo = saldo
        return self.saldo
    def get_conto_corrente(self):
        return self.nome, self.cognome, self.saldo
    def set_conto_corrente(self, nome, cognome, saldo):
        self.nome = nome
        self.cognome = cognome
        self.saldo = saldo
        return self.nome, self.cognome, self.saldo
    def prelievo(self, importo):
        self.saldo -= importo
        return self.saldo
    def versamento(self, importo):
        self.saldo += importo
        return self.saldo
    def uguale(self, altro):
        return self.nome == altro.nome and self.cognome == altro.cognome and self.saldo == altro.saldo