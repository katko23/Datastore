
from datetime import datetime

data_creation = []
data_update = []
data_delete = []
data_received = []
data_time = []
data = []
def DataCreation(clientData):
    if clientData['id'] == 666:
        return 1
    for d in data:
        if d['id'] == clientData['id']:
            return 1
    data.append(clientData)
    data_time.append(datetime.now())
    return 0


def DataUpdate(clientData):
    counter = 0
    for d in data:
        if d['id'] == clientData['id']:
            d['data'] = clientData['data']
            data_time[counter] = datetime.now()
            return 0
    counter += 1
    return 1

def DataRead(clientData):
    if clientData['id'] == 666:
        return data
    for d in data:
        if d['id'] == clientData['id']:
            return d
    return 1

def DataDelete(clientData):
    datatemp = data.copy()
    for d in datatemp:
        if d['id'] == clientData['id']:
            data.remove(d)
            return 0
    return 1

def foundId(id):
    for d in data:
        if d['id'] == id:
            return True
    return False