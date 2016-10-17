import sys
try:
    import requests
except:
    sys.path.append("lib")
    import requests
    
import json
import random
import variables as v
import ast
import threading

def queue():
    key = random.random()
    payload = {"key": key}
    jpayload = json.dumps(str(payload))
    r = requests.post(v.server + "connect/", data=jpayload)
    data = ast.literal_eval(r.text)
    if data["key"] == key:
        v.unid = data["unid"]
        t1 = threading.Thread(target=checkQueue)
        t1.start()
        
def checkQueue():
    while True:
        payload = {"unid": v.unid}
        jpayload = json.dumps(str(payload))
        r = requests.post(v.server + "check_queue/", data=jpayload)
        data = ast.literal_eval(r.text)
        if data[0] == True:
            print(data[1])
        else:
            print("False")
