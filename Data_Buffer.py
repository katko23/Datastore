
data_creation = []
data_update = []
data_delete = []
data_received = []

data = []
def DataCreation(clientData):
    if clientData['id'] == 666:
        return 1
    for d in data:
        if d['id'] == clientData['id']:
            return 1
    data.append(clientData)
    return 0


def DataUpdate(clientData):
    for d in data:
        if d['id'] == clientData['id']:
            d['data'] = clientData['data']
            return 0
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