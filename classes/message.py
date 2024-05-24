from classes.orario import Myclock as orario
class Message:
    def __init__(self, message: str = "", orario: orario = orario(0, 0)):
        self.message = message
        self.orario = orario

    def get_message(self):
        return Message(self.message, self.orario)
    def get_text(self):
        return self.message
    def set_message(self, message: str, orario: orario):
        self.message = message
        self.orario = orario

    def clear_message(self):
        self.message = ""
        self.orario = orario(0, 0)

    def reverse_message(self):
        self.message = self.message[::-1]
        return self.message

    def count_words(self):
        return len(self.message.split())

    def is_empty(self):
        return len(self.message) == 0 or self.message.isspace() or self.orario.get_orario() == (0, 0)

    def contains_word(self, word):
        return word in self.message

    def uppercase_message(self):
        self.message = self.message.upper()
        return self.message

    def lowercase_message(self):
        self.message = self.message.lower()
        return self.message
    def replace_word(self, old_word, new_word):
        self.message = self.message.replace(old_word, new_word)
        return self.message

    def capitalize_words(self):
        self.message = " ".join(word.capitalize() for word in self.message.split())
        return self.message
