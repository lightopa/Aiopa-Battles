import sys
import time
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
#from profilehooks import profile
#from memory_profiler import profile as mprofile

def localServerCheck():
    """Will check if a local debug server is running, and if not, will default to the online server"""
    try:
        r = requests.get("http://127.0.0.1:5000/check")
        if r.text != "online":
            raise Exception("not online")
    except Exception as e:
        v.server = "http://server-lightning3105.rhcloud.com/"


def queue(loadObj):
    """Will add the user to the online queue.
    
    Args:
        loadObj (menuItems.Text): The text object that reflects the current queue state.
    """
    localServerCheck()
    def _queue():
        key = random.random()
        payload = {"key": key, "name": v.name}
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
    """Will continuously connect to the server and check if a game has been found"""
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
    """Continuously checks the server for updates, and send any local updates to the server"""
    def _gameLoop():
        while True:
            netTime = time.time()
            if v.networkHalt == True:
                return
            if v.gameTurn != None:
                sentEvents = []
                if len(v.networkEvents) > 0:
                    #print("Out events", v.networkEvents)
                    sentEvents = list(v.networkEvents)
                    payload = {"unid": v.unid, "game": v.game, "type": "update", "events": sentEvents}
                    jpayload = json.dumps(str(payload))
                    r = requests.post(v.server + "game_loop/", data=jpayload)
                else:
                    payload = {"unid": v.unid, "game": v.game, "type": "fetch"}
                    jpayload = json.dumps(str(payload))
                    r = requests.post(v.server + "game_loop/", data=jpayload)
                if r.status_code != 200:
                    print(r.status_code)
                    print(r.text)
                else:
                    v.networkEvents = [e for e in v.networkEvents if not e in sentEvents]
                    data = ast.literal_eval(r.text)
                    #if data["events"] != []:
                    #    print("In events", data["events"])
                    v.networkChanges.extend(data["events"])
            #print("Network Time:", time.time() - netTime)
            v.ping.append(time.time() - netTime)
            while time.time() - netTime < 0.3:
                pass
    
    t3 = threading.Thread(target=_gameLoop)
    t3.start()

def gameJoin():
    """Will confirm the client's connection to the game server, and receive which player will begin"""
    def _gameJoin():
        payload = {"unid": v.unid, "game": v.game}
        jpayload = json.dumps(str(payload))
        r = requests.post(v.server + "game_start/", data=jpayload)
        data = ast.literal_eval(r.text)
        v.gameStarter = data["starter"]
        v.gameTurn = data["turn"]
        v.opUnid = data["opponent"]
        v.opName = data["opName"]
    t2 = threading.Thread(target=_gameJoin)
    t2.start()

def getCards():
    """Will connect to the server and download the list of cards"""
    r = requests.get(v.server + "get_cards/")
    data = ast.literal_eval(r.text)
    for value in data["cards"]:
        v.cards[value["id"]] = gameItems.card(value)
    

def changes():
    for event in v.networkChanges:
        if event["type"] == "place":
            pos = event["position"]
            pos = (3 - pos[0], pos[1])
            cunid = event["unid"]
            for tile in v.tiles:
                if tile.pos == pos:
                    target = tile
            card = v.cards[event["id"]]
            gameItems.add_card(card, tile=target, unid=cunid, player=v.opUnid, renSize=(100, 140))
        
        if event["type"] == "move":
            pos = event["position"]
            pos = (3 - pos[0], pos[1])
            for card in v.gameCards:
                if card.unid == event["unid"]:
                    c = card
            for tile in v.tiles:
                if tile.pos == pos:
                    c.tile = tile
        
        if event["type"] == "movable":
            for card in v.gameCards:
                if card.unid == event["unid"]:
                    c = card
            if event["movable"]:
                c.moves = 1
            else:
                c.moves = 0
        
        if event["type"] == "damage":
            for card in v.gameCards:
                if card.unid == event["unid"]:
                    c = card
            for card in v.gameCards:
                if card.unid == event["target"]:
                    t = card
            c.changes["health"] -= t.card.attack + t.changes["attack"]
            t.changes["health"] -= c.card.attack + c.changes["attack"]
            c._render((100, 140))
            t._render((100, 140))
        
        if event["type"] == "spell":
            for card in v.gameCards:
                if card.unid == event["target"]:
                    target = card
            if "damage" in event["effects"].keys():
                target.changes["health"] -= event["effects"]["damage"]
            target._render((100, 140))
                
        if event["type"] == "turn":
            v.gameTurn = event["turn"]
            for s in v.gameCards:
                if s.type == "minion":
                    if v.gameTurn["player"] == v.unid:
                        if s.player == v.unid and s.tile != None:
                            s.next_turn()
                    if v.gameTurn["player"] == v.opUnid:
                        if s.player == v.opUnid:
                            s.moves = 1
    v.networkChanges = []


