import json

import websockets

import Data_Buffer
import Setings
from Data_Buffer import data

def checkSync():
    # Opening JSON file
    f2 = open('data2.json')
    f3 = open('data3.json')

    # returns JSON object as
    # a dictionary
    data2 = json.load(f2)
    data3 = json.load(f3)

    # Iterating through the json
    # list
    counter = 0
    for i in data2:
        for f in data:
            if i['id'] == f['id'] and i['data'] != f['data']:
                async with websockets.connect(
                        "ws://" + str(Setings.hostName2) + ":" + str(Setings.WebSocket_port2) + '/internal/websocket') as websocket:
                    await websocket.send(str(i['id']))
                    mess = await websocket.recv()
                    if mess > Data_Buffer.data_time[counter]:
                        Data_Buffer.data[counter] = data2[counter]
                return mess
    counter += 1

    for i in data3:
        for f in data:
            if i['id'] == f['id'] and i['data'] != f['data']:
                async with websockets.connect(
                        "ws://" + str(Setings.hostName3) + ":" + str(Setings.WebSocket_port3) + '/internal/websocket') as websocket:
                    await websocket.send(str(i['id']))
                    mess = await websocket.recv()
                    if mess > Data_Buffer.data_time[counter]:
                        Data_Buffer.data[counter] = data3[counter]
                return mess

    # Closing file
    f2.close()
    f3.close()
    return 0
