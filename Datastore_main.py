import sys
import time
import threading
import asyncio
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

    from UDP_Mess_Serv import UDP_receiver, TCP_receiver, WebSocket_Receiver, WebSocket_Sender
    udpThread = threading.Thread(target=UDP_receiver())
    tcpThread = threading.Thread(target=TCP_receiver())
    # webSThread = threading.Thread(target=WebSocket_Receiver())
    # asyncio.run(WebSocket_Receiver())
    # time.sleep(2)
    # asyncio.run(WebSocket_Sender('127.0.0.1', Setings.WebSocket_port1, "All is good"))
    udpThread.start()
    tcpThread.start()
    # webSThread.start()

    from FTPwithThirdparties import sendFile, donwldFile
    sendFileThread = threading.Thread(target=sendFile("data" + str(Setings.server_nr) + ".json"))
    dwnldFileThread2 = threading.Thread(target=donwldFile("data2.json"))
    dwnldFileThread3 = threading.Thread(target=donwldFile("data3.json"))
    sendFileThread.start()
    dwnldFileThread2.start()
    dwnldFileThread3.start()
