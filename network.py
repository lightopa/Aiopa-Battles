import sys
import time
import pathfind
import hashlib
import os
import cProfile
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
import pickle
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
    def _queue():
        key = random.random()
        payload = {"key": key, "name": v.username}
        jpayload = json.dumps(str(payload))
        try:
            r = requests.post(v.server + "connect/", data=jpayload, timeout=1)
        except requests.Timeout:
            _queue()
            return
        if r.status_code != 200:
            v.gameStop = "bad"
            print(r.text)
            return
        data = ast.literal_eval(r.text)
        if data["key"] == key:
            v.unid = data["unid"]
            loadObj.text = "Finding Game"
            t1 = threading.Thread(name="checkQueue", target=checkQueue)
            t1.start()
    t0 = threading.Thread(name="queue", target=_queue)
    t0.start()


def checkQueue():
    """Will continuously connect to the server and check if a game has been found"""
    while True:
        payload = {"unid": v.unid}
        jpayload = json.dumps(str(payload))
        try:
            r = requests.post(v.server + "check_queue/", data=jpayload, timeout=1)
        except requests.Timeout:
            continue
        try:
            data = ast.literal_eval(r.text)
            if data[0] == True:
                v.game = data[1]
                return
            if v.networkHalt == True:
                return
        except:
            pass

gameLoopsStats = None


def gameLoop():
    """Continuously checks the server for updates, and send any local updates to the server"""
    def _gameLoop():
        prof = cProfile.Profile()
        prof.enable()
        try:
            while True:
                netTime = time.time()
                if v.networkHalt == True:
                    prof.disable()
                    global gameLoopsStats
                    gameLoopsStats = prof
                    return
                if v.gameTurn != None:
                    sentEvents = []
                    if len(v.networkEvents) > 0:
                        #print("Out events", v.networkEvents)
                        sentEvents = list(v.networkEvents)
                        if v.game == None:
                            return
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
                while time.time() - netTime < v.pingFreq:
                    time.sleep(v.pingFreq / 5)
        except SyntaxError:
            print(r.text)
            v.gameStop = "bad"
            return
    
    t3 = threading.Thread(name="gameLoop", target=_gameLoop)
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
        getAccount(v.opName)
    t2 = threading.Thread(name="gameJoin", target=_gameJoin)
    t2.start()
    
def gameLeave(reason="disconnect"):
    """Will tell the server that the client has disconnected"""
    payload = {"unid": v.unid, "game": v.game, "reason": reason}
    jpayload = json.dumps(str(payload))
    r = requests.post(v.server + "game_leave/", data=jpayload)

def getCards():
    """Will connect to the server and download the list of cards"""
    r = requests.get(v.server + "get_cards/")
    data = ast.literal_eval(r.text)
    for value in data["cards"]:
        v.cards[value["id"]] = gameItems.card(value)

def registerAccount(username, password):
    """Will register a new account with the server"""
    def _registerAccount():
        localServerCheck()
        hash_object = hashlib.md5(password.encode())
        hash = hash_object.hexdigest()
        payload = {"username": username, "password": hash}
        jpayload = json.dumps(str(payload))
        r = requests.post(v.server + "register_account/", data=jpayload)
        data = ast.literal_eval(r.text)
        v.registerSuccess = data
    tr = threading.Thread(name="register", target=_registerAccount)
    tr.start()

def updateAccount(send):
    """Will update an account's stats"""
    def _updateAccount():
        localServerCheck()
        hash_object = hashlib.md5(v.password.encode())
        hash = hash_object.hexdigest()
        payload = {"username": v.username, "password": hash, "update": send}
        jpayload = json.dumps(str(payload))
        r = requests.post(v.server + "update_account/", data=jpayload)
        data = ast.literal_eval(r.text)
    tu = threading.Thread(name="update", target=_updateAccount)
    tu.start()


def saveMetadata():
    """Will save some data to a pickled file"""
    with open("data.dat", "wb") as f:
        data = {"username": v.username,
                "password": v.password,
                "version": v.version,
                "fullscreen": v.fullscreen,
                "pingFreq": v.pingFreq,
                "debug": v.debug}
        pickle.dump(data, f)

def loadMetadata():
    """Will load data from a pickled file"""
    try:
        if os.path.exists("data.dat"):
            with open("data.dat", "rb") as f:
                data = pickle.load(f)
                v.username = data["username"]
                v.password = data["password"]
                v.fullscreen = data["fullscreen"]
                v.pingFreq = data["pingFreq"]
                v.debug = data["debug"]
    except:
        saveMetadata()
        
    
def login(username, password):
    """Will 'login' to the server"""
    def _login(count=0):
        localServerCheck()
        try:
            hash_object = hashlib.md5(password.encode())
            hash = hash_object.hexdigest()
            payload = {"username": username, "password": hash}
            jpayload = json.dumps(str(payload))
            r = requests.post(v.server + "login/", data=jpayload, timeout=1)
            data = ast.literal_eval(r.text)
            if data == True:
                getCards()
                getAccount()
            v.loggedIn = data
        except requests.exceptions.RequestException:
            count += 1
            if count > 4:
                v.timeoutStage = 1
            if count > 8:
                v.timeoutStage = 2
            _login(count)
    v.timeoutStage = 0
    tl = threading.Thread(name="login", target=_login)
    tl.start()
    
def getAccount(username=None):
    """Will get account stats from a given username"""
    if username == None:
        username = v.username
    def _getAccount():
        localServerCheck()
        payload = {"username": username}
        jpayload = json.dumps(str(payload))
        r = requests.post(v.server + "get_account/", data=jpayload)
        if username == v.username:
            v.account = ast.literal_eval(r.text)
        else:
            v.opAccount = ast.literal_eval(r.text)
    tl = threading.Thread(name="login", target=_getAccount)
    tl.start()

def changes():
    """Will implement the list of changes fetched from the game server"""
    for event in v.networkChanges:
        if v.online == False and event["type"] == "turn" and len(v.networkChanges) > 1:
            v.networkChanges.append(v.networkChanges.pop(0))
        if event["type"] == "place":
            pos = event["position"]
            pos = (3 - pos[0], pos[1])
            cunid = event["unid"]
            for tile in v.tiles:
                if tile.pos == pos:
                    target = tile
            card = v.cards[event["id"]]
            gameItems.add_card(card, tile=target, unid=cunid, player=v.opUnid, renSize=(100, 140), opintro=True)
        
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
        
        if event["type"] == "movable" or "movable" in event.keys():
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
                    if v.gameTurn["player"] == v.unid: # If player's turn
                        if s.player == v.unid and s.tile != None:
                            s.next_turn()
                    if v.gameTurn["player"] == v.opUnid: # If opponent's turn
                        if s.player == v.opUnid:
                            s.moves = 1
            if v.gameTurn["player"] == v.unid: # If player's turn
                if len(v.hand) < 4:
                    for card in v.gameDeck:
                        if card.order == 0:
                            card.aniCycle = 1
                        else:
                            card.order -= 1
                v.pturn.cycle = 1
                if v.totalMana < 10:
                    v.totalMana += 1
                v.pMana = v.totalMana
        if event["type"] == "stop":
            v.gameStop = event["reason"]
            v.networkHalt = True
        
        if v.online == False:
            v.networkChanges.remove(event)
            return
    v.networkChanges = []