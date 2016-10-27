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
import gameItems

def localServerCheck():
    try:
        r = requests.get("http://127.0.0.1:5000/check")
        if r.text != "online":
            raise Exception("not online")
    except Exception as e:
        v.server = "http://server-lightning3105.rhcloud.com/"


def queue(loadObj):
    localServerCheck()
    def _queue():
        key = random.random()
        payload = {"key": key}
        jpayload = json.dumps(str(payload))
        r = requests.post(v.server + "connect/", data=jpayload)
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
        if v.networkHalt == True:
            return

def gameLoop():
    def _gameLoop():
        payload = {"unid": v.unid, "game": v.game}
        jpayload = json.dumps(str(payload))
        r = requests.post(v.server + "game_loop/", data=jpayload)
        data = ast.literal_eval(r.text)
    
    if v.serverConnected:
        t3 = threading.Thread(target=_gameLoop)
        t3.start()
        
        
def gameJoin():
    def _gameJoin():
        payload = {"unid": v.unid, "game": v.game} #also push name
        jpayload = json.dumps(str(payload))
        r = requests.post(v.server + "game_start/", data=jpayload)
        data = ast.literal_eval(r.text)
        v.gameStarter = data["starter"]
        v.gameTurn = data["turn"]
        print(v.gameStarter, v.gameTurn)
    t2 = threading.Thread(target=_gameJoin)
    t2.start()

def getCards():
    print(v.server + "get_cards/")
    r = requests.get(v.server + "get_cards/")
    data = ast.literal_eval(r.text)
    for value in data["cards"]:
        v.cards[value["name"]] = gameItems.card(name=value["name"], 
                                                attack=value["attack"],
                                                health=value["health"],
                                                speed=value["speed"],
                                                description=value["description"],
                                                type=value["type"],
                                                cost=value["cost"])
    print(v.cards)
    