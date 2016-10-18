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

def localServerCheck():
    try:
        r = requests.get("http://127.0.0.1:5000/")
        print(r.status_code)
        if r.status_code == 404:
            raise Exception()
    except:
        v.server = "http://server-lightning3105.rhcloud.com/"
    print(v.server)


def queue(loadObj):
    localServerCheck()
    def _queue():
        key = random.random()
        payload = {"key": key}
        jpayload = json.dumps(str(payload))
        print("start")
        r = requests.post(v.server + "connect/", data=jpayload)
        print("end")
        data = ast.literal_eval(r.text)
        if data["key"] == key:
            v.unid = data["unid"]
            loadObj.text = "Finding Game"
            t1 = threading.Thread(target=checkQueue)
            t1.start()
    t0 = threading.Thread(target=_queue)
    t0.start()


def checkQueue():
    while True:
        payload = {"unid": v.unid}
        jpayload = json.dumps(str(payload))
        r = requests.post(v.server + "check_queue/", data=jpayload)
        data = ast.literal_eval(r.text)
        if data[0] == True:
            v.game = data[1]
            return

#def getCards():
    