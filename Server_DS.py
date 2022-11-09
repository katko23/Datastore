from threading import Thread
import threading
import requests
from flask import Flask, request,  jsonify
import Reqs
import Setings
from Data_Buffer import data_received,DataCreation,DataRead,DataUpdate,DataDelete

hostName = Setings.serverName
serverPort = Setings.this_serverPort
server_nr = Setings.server_nr

class Server(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        app = Flask(__name__)

        @app.route('/DS', methods=['GET', 'POST'])
        def client_endpoint():
            input_json = request.get_json(force=True)
            # force=True, above, is necessary if another developer
            # forgot to set the MIME type to 'application/json'
            print('data from client:', input_json)
            serverLock = threading.Lock()
            serverLock.acquire()
            data_received.append(input_json)
            dictToReturn = {}
            if input_json['action'] == 'create':
                res = requests.post("http://" + str(Setings.hostName2) + ":" + str(Setings.serverPort2) + "/internal", json=input_json)
                print('response from server:', res.text)
                res = requests.post("http://" + str(Setings.hostName3) + ":" + str(Setings.serverPort3) + "/internal", json=input_json)
                print('response from server:', res.text)
                clientData = input_json.copy()
                clientData.pop('action')
                error = DataCreation(clientData)
                if error == 0:
                    dictToReturn = {"Mess": " Command creation is done"}
                else:
                    dictToReturn = {"Error": " Change Id , it's already in use"}
            if input_json['action'] == 'read':
                clientData = input_json.copy()
                clientData.pop('action')
                data = DataRead(clientData)
                dictToReturn = { "Storage" : data}
                if data == 1:
                    dictToReturn = {"Error": " Data with this id is not found"}
            if input_json['action'] == 'update':
                clientData = input_json.copy()
                clientData.pop('action')
                error = DataUpdate(clientData)
                if error == 0:
                    dictToReturn = {"Mess": " Command update is done"}
                else:
                    dictToReturn = {"Error": " Data with this id is not found"}
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


        @app.route('/internal', methods=['GET', 'POST'])
        def internal_endpoint():
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
            if input_json['action'] == 'read':
                clientData = input_json.copy()
                clientData.pop('action')
                data = DataRead(clientData)
                dictToReturn = {"Storage": data}
                if data == 1:
                    dictToReturn = {"Error": " Data with this id is not found"}
            if input_json['action'] == 'update':
                clientData = input_json.copy()
                clientData.pop('action')
                error = DataUpdate(clientData)
                if error == 0:
                    dictToReturn = {"Mess": " Command update is done"}
                else:
                    dictToReturn = {"Error": " Data with this id is not found"}
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

        app.run(host=hostName, port=serverPort, debug=False)