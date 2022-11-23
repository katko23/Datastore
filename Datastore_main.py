import sys
import threading
from CheckMain import checkMain
import Setings

if __name__ == "__main__":
    check = threading.Lock()
    check.acquire()
    checkMain()
    check.release()
    import Server_DS
    server = Server_DS.Server()
    server.start()
    from UDP_Mess_Serv import UDP_receiver, TCP_receiver
    udpThread = threading.Thread(target=UDP_receiver())
    tcpThread = threading.Thread(target=TCP_receiver())
    udpThread.start()
    tcpThread.start()
