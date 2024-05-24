from classes.message import Message
from classes.orario import Myclock


if __name__ == '__main__':
    messaggio = Message("ciao", Myclock(12, 30))
    print(messaggio)