import socket
import sys
import Setings

ip_sender = Setings.UDP_Serv
port_sender = Setings.UDP_port

def receiver():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ip_sender, port_sender))
    print("Start UDP Server with sockets")
    while True:
        try:
            msg = s.recvfrom(1024)
            print("\n" + msg[0].decode())
            if "exit" in msg[0].decode() or "bye" in msg[0].decode():
                sys.exit()
        except:
            pass

