class BankAccount:
    def __init__(self, name, surname, balance):
        self.name = name
        self.surname = surname
        self.balance = balance
    def get_balance(self):
        return self.balance
    def set_balance(self, balance):
        self.balance = balance
        return self.balance
    def get_bank_account(self):
        return self.name, self.surname, self.balance
    def set_bank_account(self, name, surname, balance):
        self.name = name
        self.surname = surname
        self.balance = balance
        return self.name, self.surname, self.balance
    def withdraw(self, amount):
        self.balance -= amount
        return self.balance
    def deposit(self, amount):
        self.balance += amount
        return self.balance
    def equal(self, other):
        return self.name == other.name and self.surname == other.surname and self.balance == other.balance
