import sys
import time
import pathfind
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
        if r.status_code != 200:
            v.gameStop = "bad"
            print(r.text)
            return
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
        try:
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
        except SyntaxError:
            print(r.text)
            v.gameStop = "bad"
            return
    
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
    
def gameLeave():
    """Will tell the server that the client has disconnected"""
    payload = {"unid": v.unid, "game": v.game}
    jpayload = json.dumps(str(payload))
    r = requests.post(v.server + "game_leave/", data=jpayload)

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
            c = None
            for card in v.gameCards:
                if card.unid == event["unid"]:
                    c = card
            if c == None:
                continue
            for tile in v.tiles:
                if tile.pos == pos:
                    path = pathfind.pathfind(c.tile.pos, pos, pathfind.get_grid())
                    c.tile = tile
            
            c.movePath = path
        
        if event["type"] == "movable":
            c = None
            for card in v.gameCards:
                if card.unid == event["unid"]:
                    c = card
            if c == None:
                continue
            if event["movable"]:
                c.moves = 1
            else:
                c.moves = 0
        
        if event["type"] == "damage":
            for card in v.gameCards:
                if card.unid == event["unid"]:
                    c = card
            if event["target"] == v.unid:
                v.pHealth -= c.card.attack + c.changes["attack"]
                c.attack("player")
            else:
                for card in v.gameCards:
                    if card.unid == event["target"]:
                        t = card
                c.changes["health"] -= t.card.attack + t.changes["attack"]
                t.changes["health"] -= c.card.attack + c.changes["attack"]
                c.attack(t)
            #c._render((100, 140))
            #t._render((100, 140))
        
        if event["type"] == "spell":
            for card in v.gameCards:
                if card.unid == event["target"]:
                    target = card
            if "damage" in event["effects"].keys():
                target.changes["health"] -= event["effects"]["damage"]
            
            gameItems.Effect(event["animation"], target=target, sheet="assets/images/effects/fireball.png")
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
            if v.gameTurn["player"] == v.unid:
                for card in v.gameDeck:
                    if card.order == 0:
                        card.aniCycle = 1
                    else:
                        card.order -= 1
                v.pturn.cycle = 1
        if event["type"] == "stop":
            v.gameStop = event["reason"]
            v.networkHalt = True
    v.networkChanges = []