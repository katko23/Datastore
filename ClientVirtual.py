import requests
import os
import Setings
import time


def Create(data_id , data):
    dictToSend = {"id": data_id, "action" : "create" , "data": data}
    res = requests.post("http://" + str(Setings.hostName) + ":" + str(Setings.this_serverPort) + "/DS1", json=dictToSend)
    print('response from server:', res.text)

def Read(data_id):
    dictToSend = {"id": data_id, "action" : "read"}
    res = requests.post("http://" + str(Setings.hostName) + ":" + str(Setings.this_serverPort) + "/DS1", json=dictToSend)
    print('In your database you have :', res.text)

def Update(data_id , data):
    dictToSend = {"id": data_id, "action" : "update" , "data": data}
    res = requests.post("http://" + str(Setings.hostName) + ":" + str(Setings.this_serverPort) + "/DS1", json=dictToSend)
    print('response from server:', res.text)

def Delete(data_id):
    dictToSend = {"id": data_id, "action" : "delete"}
    res = requests.post("http://" + str(Setings.hostName) + ":" + str(Setings.this_serverPort) + "/DS1", json=dictToSend)
    print('response from server:', res.text)

def CMD_Menu():
    while True :
        os.system('cls')
        print("You can chose one of this :")
        print("* Create \n* Read \n* Update \n* Delete")
        print("In order to do something , write what you wanna do , write id of data ( for C , U and D) \n "
              "and write for C and D what data you wanna add or update ")

        cmd = input("Please enter instruction: ")
        print("You entered: " + cmd)
        var = cmd.split()
        commands_list = var.copy()
        if len(var) > 1:
            var.pop(0)
        if var.pop(0).isnumeric() == False:
            print("id gresit ( e necesar numar integer )")
            time.sleep(10)
            continue
        if commands_list[0] == 'Create' or commands_list[0] == 'create':
            data = ""
            for d in var:
                data = data + " " + d
            Create(int(commands_list[1]), data)
        if commands_list[0] == 'Read' or commands_list[0] == 'read':
            Read(int(commands_list[1]))
        if commands_list[0] == 'Update' or commands_list[0] == 'update':
            data = ""
            for d in var:
                data = data + " " + d
            Update(int(commands_list[1]), data)
        if commands_list[0] == 'Delete' or commands_list[0] == 'delete':
            Delete(int(commands_list[1]))

def clientUDP():
    import socket

    UDP_IP = '127.0.0.1'
    UDP_PORT = 27003
    MESSAGE = "Hello, World!"

    print("UDP target IP: %s" % UDP_IP)
    print("UDP target port: %s" % UDP_PORT)
    print("message: %s" % MESSAGE)

    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))

if __name__ == "__main__":
    # CMD_Menu()
    clientUDP()