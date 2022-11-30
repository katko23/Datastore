from threading import Thread
import threading
import requests
from flask import Flask, request,  jsonify
from flask_sock import Sock

import Data_Buffer
import Reqs
import Setings
import UDP_Mess_Serv
from UDP_Mess_Serv import TCP_sender, UDP_sender
import Switch
from Data_Buffer import data_received,DataCreation,DataRead,DataUpdate,DataDelete

hostName = Setings.serverName
serverPort = Setings.this_serverPort
server_nr = Setings.server_nr

class Server(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        app = Flask(__name__)
        sock = Sock(app)
        cl_add = Switch.CounterS(1,2,3)

        @app.route('/DS', methods=['GET'])
        def client_read():
            input_json = request.get_json(force=True)
            # force=True, above, is necessary if another developer
            # forgot to set the MIME type to 'application/json'
            print('data from client:', input_json)
            serverLock = threading.Lock()
            serverLock.acquire()
            data_received.append(input_json)
            dictToReturn = {}
            if input_json['action'] == 'read':
                clientData = input_json.copy()
                clientData.pop('action')
                data = []
                if isinstance(DataRead(clientData),list):
                    data = DataRead(clientData)
                else :
                    data.append(DataRead(clientData))
                res = requests.get("http://" + str(Setings.hostName2) + ":" + str(Setings.serverPort2) + "/internal",
                                    json=input_json)
                datar = res.json()
                if 'Error' in datar:
                    pass
                else:
                    listTemp = []
                    if isinstance(datar['Storage'], list):
                        listTemp = datar['Storage']
                    else:
                        listTemp.append(datar['Storage'])
                    data = data + listTemp
                res = requests.get("http://" + str(Setings.hostName3) + ":" + str(Setings.serverPort3) + "/internal",
                                    json=input_json)
                datar = res.json()
                if 'Error' in datar:
                    pass
                else:
                    listTemp = []
                    if isinstance(datar['Storage'], list):
                        listTemp = datar['Storage']
                    else :
                        listTemp.append(datar['Storage'])
                    data = data + listTemp
                print(data)
                result = list(
                    {
                        dictionary['id']: dictionary
                        for dictionary in data
                    }.values()
                )
                print(result)
                dictToReturn = { "Storage" : result}
                if data == 1:
                    dictToReturn = {"Error": " Data with this id is not found"}
            serverLock.release()
            return jsonify(dictToReturn)

        @app.route('/DS', methods=['POST'])
        def client_add():
            input_json = request.get_json(force=True)
            # force=True, above, is necessary if another developer
            # forgot to set the MIME type to 'application/json'
            print('data from client:', input_json)
            serverLock = threading.Lock()
            serverLock.acquire()
            data_received.append(input_json)
            dictToReturn = {"Error": " Change Id , it's already in use"}
            error = 0
            if UDP_sender('create', input_json['id']):
                error = 0
                print ("All it's good no such ID")
            else:
                error = 1
                print (" Error change Id ")

            # if TCP_sender('create', input_json['id'], Setings.UDP_Serv2,Setings.TCP_port1) and TCP_sender('create', input_json['id'], Setings.UDP_Serv3, Setings.TCP_port2):
            #     error = 0
            # else:
            #     error = 1

            if input_json['action'] == 'create' and error == 0:
                if cl_add.i2 != 3 :
                    res = requests.post("http://" + str(Setings.hostName2) + ":" + str(Setings.serverPort2) + "/internal",
                                    json=input_json)
                    print('response from server:', res.text)
                    if "Error" in res.json():
                        error = 1
                if cl_add.i3 != 3 :
                    res = requests.post("http://" + str(Setings.hostName3) + ":" + str(Setings.serverPort3) + "/internal",
                                    json=input_json)
                    print('response from server:', res.text)
                    if "Error" in res.json():
                        error = 1
                if cl_add.i1 != 3 and error == 0:
                    clientData = input_json.copy()
                    clientData.pop('action')
                    error = DataCreation(clientData)
                if error == 0:
                    dictToReturn = {"Mess": " Command creation is done"}
                    cl_add.Pass()
                else:
                    dictToReturn = {"Error": " Change Id , it's already in use"}
            serverLock.release()
            return jsonify(dictToReturn)

        @app.route('/DS', methods=['PUT'])
        def client_change():
            input_json = request.get_json(force=True)
            # force=True, above, is necessary if another developer
            # forgot to set the MIME type to 'application/json'
            print('data from client:', input_json)
            serverLock = threading.Lock()
            serverLock.acquire()
            data_received.append(input_json)
            dictToReturn = {}
            if input_json['action'] == 'update':
                clientData = input_json.copy()
                clientData.pop('action')
                error = DataUpdate(clientData)
                res = requests.put("http://" + str(Setings.hostName2) + ":" + str(Setings.serverPort2) + "/internal",
                                   json=input_json)
                datar = res.json()
                if 'Error' in datar:
                    pass
                elif error == 1 :
                    error = 0
                res = requests.put("http://" + str(Setings.hostName3) + ":" + str(Setings.serverPort3) + "/internal",
                                   json=input_json)
                datar = res.json()
                if 'Error' in datar:
                    pass
                elif error == 1:
                    error = 0

                if error == 0:
                    dictToReturn = {"Mess": " Command update is done"}
                else:
                    dictToReturn = {"Error": " Data with this id is not found"}
            serverLock.release()
            return jsonify(dictToReturn)

        @app.route('/DS', methods=['DELETE'])
        def client_delete():
            input_json = request.get_json(force=True)
            # force=True, above, is necessary if another developer
            # forgot to set the MIME type to 'application/json'
            print('data from client:', input_json)
            serverLock = threading.Lock()
            serverLock.acquire()
            data_received.append(input_json)
            dictToReturn = {}
            if input_json['action'] == 'delete':
                clientData = input_json.copy()
                clientData.pop('action')
                error = DataDelete(clientData)

                res = requests.post("http://" + str(Setings.hostName2) + ":" + str(Setings.serverPort2) + "/internal",
                                   json=input_json)
                datar = res.json()
                if 'Error' in datar:
                    pass
                elif error == 1:
                    error = 0
                res = requests.post("http://" + str(Setings.hostName3) + ":" + str(Setings.serverPort3) + "/internal",
                                   json=input_json)
                datar = res.json()
                if 'Error' in datar:
                    pass
                elif error == 1:
                    error = 0

                if error == 0:
                    dictToReturn = {"Mess": " Command delete is done"}
                else:
                    dictToReturn = {"Error": " Data with this id is not found"}
            serverLock.release()
            return jsonify(dictToReturn)

        @app.route('/internal', methods=['POST'])
        def internal_create():
            input_json = request.get_json(force=True)
            print('data from server:', input_json)
            serverLock = threading.Lock()
            serverLock.acquire()
            data_received.append(input_json)
            dictToReturn = {}
            if input_json['action'] == 'create':
                clientData = input_json.copy()
                clientData.pop('action')
                error = DataCreation(clientData)
                if error == 0:
                    dictToReturn = {"Mess": " Command creation is done"}
                else:
                    dictToReturn = {"Error": " Change Id , it's already in use"}
            if input_json['action'] == 'delete':
                clientData = input_json.copy()
                clientData.pop('action')
                error = DataDelete(clientData)
                if error == 0:
                    dictToReturn = {"Mess": " Command delete is done"}
                else:
                    dictToReturn = {"Error": " Data with this id is not found"}

            serverLock.release()
            return jsonify(dictToReturn)

        @app.route('/internal', methods=['GET'])
        def internal_read():
            input_json = request.get_json(force=True)
            print('data from server:', input_json)
            serverLock = threading.Lock()
            serverLock.acquire()
            data_received.append(input_json)
            dictToReturn = {}
            if input_json['action'] == 'read':
                clientData = input_json.copy()
                clientData.pop('action')
                data = DataRead(clientData)
                dictToReturn = {"Storage": data}
                if data == 1:
                    dictToReturn = {"Error": " Data with this id is not found"}
            serverLock.release()
            return jsonify(dictToReturn)

        @app.route('/internal', methods=['PUT'])
        def internal_change():
            input_json = request.get_json(force=True)
            print('data from server:', input_json)
            serverLock = threading.Lock()
            serverLock.acquire()
            data_received.append(input_json)
            dictToReturn = {}
            if input_json['action'] == 'update':
                clientData = input_json.copy()
                clientData.pop('action')
                error = DataUpdate(clientData)
                if error == 0:
                    dictToReturn = {"Mess": " Command update is done"}
                else:
                    dictToReturn = {"Error": " Data with this id is not found"}
            serverLock.release()
            return jsonify(dictToReturn)

            serverLock.release()
            return jsonify(dictToReturn)

        @sock.route('/internal/websocket')
        def echo(sock):
            while True:
                data = sock.receive()
                print(data)
                response = Data_Buffer.data_time[data]
                sock.send(response)

        app.run(host=hostName, port=serverPort, debug=False,  use_reloader=False)