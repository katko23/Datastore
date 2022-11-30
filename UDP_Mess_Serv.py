import socket
import sys
import time
import asyncio
import websockets
import Setings
import pickle
from Data_Buffer import foundId

ip_sender = Setings.UDP_Serv1
udp_port_sender = Setings.UDP_port1
tcp_ip_sender = Setings.TCP_ip1
tcp_port_sender = Setings.TCP_port1

buffer_udp = True

def UDP_receiver():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ip_sender, udp_port_sender))
    print("Start UDP Server with sockets")
    global buffer_udp
    while True:
        try:
            msg = s.recvfrom(1024)
            print("\n" + msg[0].decode())
            data_to_send = "Okey"
            print(msg[0].decode())
            if "exit" in msg[0].decode() or "bye" in msg[0].decode():
                sys.exit()
            if "Create" in msg[0].decode():
                bitStr = msg[0].decode()
                stringarr = bitStr.split(":")
                if foundId(int(stringarr[1])):
                    data_to_send = "Error"
                s.sendto(data_to_send.encode(), (Setings.UDP_Serv1, Setings.UDP_port1))
            if "Error" in msg[0].decode():
                buffer_udp = False
        except:
            pass


def TCP_receiver():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((tcp_ip_sender, tcp_port_sender))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                # data_to_send = 'Empty'
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break
                else:
                    pass
                    # dict = pickle.loads(data)
                    # if 'create' in dict:
                    #     if foundId(dict[id]):
                    #         data_to_send = 'Error'
                data_to_send = bytes(data_to_send, 'utf-8')
                conn.sendall(data)


def UDP_sender(action, id):
    global buffer_udp
    if(action == 'create'):
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        sock.sendto(("Create id: \n " + str(id)).encode(), (Setings.UDP_Serv2, Setings.UDP_port2))
        sock.sendto(("Create id: \n " + str(id)).encode(), (Setings.UDP_Serv3, Setings.UDP_port3))
        time.sleep(0.1)
        if buffer_udp:
            return True
        else:
            return False


def TCP_sender(action, id, HOST, PORT):
    if(action == 'create'):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            dictToSend = {'action': 'create', 'id':id }
            s.sendall(pickle.dumps(dictToSend))
            data = s.recv(1024)
        print(f"Received {data!r}")
        res = str(data, 'utf-8')
        if res == 'Error':
            return False
        else:
            return True


async def webSocketecho(websocket):
    async for message in websocket:
        await websocket.send(message)
        print(message)

async def WebSocket_Receiver():
    async with websockets.serve(webSocketecho, port=Setings.WebSocket_port1):
        await asyncio.Future()  # run forever

async def WebSocket_Sender(ws_host, ws_port, mess):
    async with websockets.connect("ws://" + str(ws_host) + ":" + str(ws_port)) as websocket:
        await websocket.send(mess)
        await websocket.recv()


