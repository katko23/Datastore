import Server_DS
import threading
from UDP_Mess_Serv import receiver

if __name__ == "__main__":

    server = Server_DS.Server()
    server.start()

    receiver()
