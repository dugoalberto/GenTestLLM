import random

from classes.message import Message
from classes.orario import Myclock
from classes.chat import myChat

if __name__ == '__main__':
    messaggi = []
    for i in range(10):
        messaggi.append(Message("ciao"+str(i), Myclock(12, 30)))
    chat = myChat(messaggi)
    chat.replace_messages(Message("ciao1", Myclock(12, 30)), Message("ciao2", Myclock(12, 30)))
    print(chat.get_messages())
