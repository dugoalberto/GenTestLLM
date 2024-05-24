import classes.message as Message
class myChat:
    def __init__(self, messages: [Message]):
        self.messages = messages
    def add_message(self, message: Message):
        self.messages.append(message)
        return self.messages
    def get_messages(self):
        return self.messages
    def clear_messages(self):
        self.messages = []
        return self.messages
    def count_messages(self):
        return len(self.messages)
    def is_empty(self):
        return len(self.messages) == 0
    def contains_message(self, message: Message):
        return message in self.messages
    def uppercase_messages(self):
        self.messages = [message.uppercase_message() for message in self.messages]
        return self.messages
    def lowercase_messages(self):
        self.messages = [message.lowercase_message() for message in self.messages]
        return self.messages
    def replace_messages(self, old_message: Message, new_message: Message):
        old_text= old_message.get_text()

        new_message= new_message.get_text()
        new_message = new_message.upper()
        new_message = new_message[::-1]

        self.messages = [message.replace_word(old_text, new_message) for message in self.messages]
        return self.messages
    def capitalize_messages(self):
        self.messages = [message.capitalize_message() for message in self.messages]
        return self.messages

