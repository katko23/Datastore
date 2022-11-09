import socket

import Setings


def internet(host=str(Setings.server_main_hname), port= Setings.server_main_port , timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(ex)
        return False

def checkMain():
    while Setings.this_serverPort != Setings.server_main_port:
        if internet() == False :
            Setings.serverName = Setings.server_main_hname
            Setings.this_serverPort = Setings.server_main_port
            print(Setings.serverName , Setings.this_serverPort)
        else:
            break
