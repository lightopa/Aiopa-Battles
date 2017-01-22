import variables as v
import time
import random
import pathfind

def ai():
    for event in v.networkEvents:
        if event["type"] == "turn":
            v.networkChanges.append({"type": "turn", "turn": {"player": v.opUnid, "time": time.time()}})
            if len(v.opDeck) > 0:
                v.opHand.append(v.opDeck.pop(0))
            v.opMana = v.totalMana
            for s in v.gameCards:
                if s.type == "minion":
                    if s.player == 0:
                        s.next_turn()
            ai_move()
            v.networkEvents.remove(event)
            
            v.networkChanges.append({"type": "turn", "turn": {"player": v.unid, "time": time.time()}})
    
def ai_move():
    board = [["", "", "", ""],
             ["", "", "", ""],
             ["", "", "", ""]]
    
    for card in v.gameCards:
        if card.tile != None:
            board[card.tile.pos[1]][card.tile.pos[0]] = card
    
    playableCards = [c for c in v.opHand if c.cost <= v.opMana]
    
    control = ai_control(board)
    
    priorities = ai_priorities(board)
    
    for y in range(3):
        for x in range(4):
            if board[y][x] != "" and board[y][x].player == 0 and board[y][x].moves > 0:
                ai_action(board, board[y][x], priorities)
                
    
    if control[0] < 2 * v.aiMod["placeMinionMod"]:
        for p in playableCards:
            if p.type == "minion" and p.cost <= v.opMana:
                while True:
                    pos = (random.randint(2, 3), random.randint(0, 2))
                    if board[pos[1]][pos[0]] == "":
                        unid = "c" + str(v.opUnid) + str(v.cardUnid)
                        v.cardUnid += 1
                        v.networkChanges.append({"type": "place", "id": p.id, "position": ai_invertCoords(pos), "unid": unid})
                        v.opMana -= p.cost
                        break

def print_board(board):
    print("_________")
    for y in board:
        print(y)

def ai_control(board):
    #Perhaps the number of enemy minions each player could kill
    aiControl = 1
    pControl = 1
    for y in board:
        for x in y:
            c = x
            if c != "":
                if c.player == 0:
                    aiControl += ai_rank(c, hmod=1, mxhmod=0)
                else:
                    pControl += ai_rank(c, hmod=1, mxhmod=0)
    ratio = aiControl / pControl
    return ratio, aiControl, pControl

def ai_rank(c, hmod=1, mxhmod=1):
    out = ((c.card.cost * v.aiMod["c_costMod"])
             + ((c.card.attack + c.changes["attack"]) * v.aiMod["c_attackMod"])
             + ((c.card.health + c.changes["health"]) * v.aiMod["c_healthMod"] * hmod)
             + ((c.card.health / (c.card.health + c.changes["health"])) * v.aiMod["c_mxHealthMod"] * mxhmod))
    
    path = pathfind.pathfind(c.tile.pos, (-1, 1), pathfind.get_grid(castle=True))
    if path != False:
        while path[-1][0] > 3 and path[-2][0] > 3:
            path = path[:-1]
        if len(path) >= c.card.speed + c.changes["speed"] or c.tile.pos[0] + c.tile.range >= 4:
            out += ((c.card.attack + c.changes["attack"]) * v.aiMod["c_attackMod"])
            out += (20 / v.opHealth) * v.aiMod["p_castleMod"]
        
    return out

def ai_priorities(board):
    targets = []
    for y in board:
        for x in y:
            c = x
            if c != "":
                rank = ai_rank(c, mxhmod=v.aiMod["p_mxHealthMod"], hmod=v.aiMod["p_healthMod"])
                if c.player == 0:
                    targets.append({"card": c, "rank": rank, "action": "help"})
                else:
                    targets.append({"card": c, "rank": rank, "action": "attack"})
    rank = (20 / v.opHealth) * v.aiMod["p_castleMod"]
    targets.append({"card": "aiCastle", "rank": rank, "action": "help"})
    
    rank = (20 / v.pHealth) * v.aiMod["p_castleMod"] + v.aiMod["playerCastleAdd"]
    targets.append({"card": "pCastle", "rank": rank, "action": "attack"})
    
    #print([t for t in targets if t["action"] != "help"])
    return targets

def ai_action(board, c, targets):
    bestAction = (None, 0)
    #print("====", c.card.id, c.tile.pos, "====")
    for y in range(3):
        for x in range(-1, 4):
            curRank = 0
            path = pathfind.pathfind((c.tile.pos[0] + 1, c.tile.pos[1]), (x + 1, y), pathfind.get_grid(skip=[(x, y)], castle=True))
            #print(">>", (x, y))
            if path != False:
                path = [(p[0]-1, p[1]) for p in path]
                card = board[y][x] # Card is actually a tile... oops
                if card != "" or x == -1 or x == 4 and (x, y) != c.tile.pos:
                    if len(path) > 1:
                        while path[-2][0] > 3 or path[-2][0] < -1:
                            path = path[:-1]
                    if x == -1:
                        curRank = [t["rank"] for t in targets if t["card"] == "pCastle"][0]
                    elif x == 4:
                        curRank = [t["rank"] for t in targets if t["card"] == "aiCastle"][0]
                    elif card != "":
                        for t in targets:
                            if t["card"] == card and t["card"].player != 0:
                                curRank += t["rank"]
                    else:
                        curRank = 0
                    speedDiff = len(path) - c.card.speed + c.changes["speed"]
                    if speedDiff > 0:
                        curRank -= speedDiff * v.aiMod["m_moveDiffMod"]
                    
                    #print("----", curRank, path)
                    
                    if curRank > bestAction[1]:
                        #print("^^^^ overtake")
                        while len(path) > c.card.speed + c.changes["speed"] + 1:
                            path = path[:-1]
                        
                        event = []
                        if len(path) != 0 and c.card.speed + c.changes["speed"] > 0:
                            if path[-1][0] == -1 or path[-1][0] == 4:
                                while len(path) > 0 and (path[-1][0] < 0 or path[-1][0] > 3):
                                    path = path[:-1]
                                if len(path) > 1:
                                    event.append({"type": "move", "unid": c.unid, "position": ai_invertCoords(path[-1])})
                                if len(path) == 0 or path[-1][0] == -1:
                                    event.append({"type": "damage", "unid": c.unid, "target": v.unid})
                                    #print("++++ damage castle")
                            else:
                                target = board[path[-1][1]][path[-1][0]]
                                if target != "":
                                    if len(path) > 1:
                                        event.append({"type": "move", "unid": c.unid, "position": ai_invertCoords(path[-2])})
                                    event.append({"type": "damage", "unid": c.unid, "target": target.unid})
                                    #print("++++ damage", target.unid, target.tile.pos, (path[-1][0], path[-1][1]))
                                    if c.range == 0 and target.changes["health"] + target.card.health - (c.card.attack + c.changes["attack"]) <= 0 and c.changes["health"] + c.card.health - (target.card.attack + target.changes["attack"]) > 0:
                                        event[-1]["kill"] = True
                                        event.append({"type": "move", "unid": c.unid, "position": ai_invertCoords(target.tile.pos)})
                                else:
                                    event.append({"type": "move", "unid": c.unid, "position": ai_invertCoords(path[-1])})
                            bestAction = (event, curRank)
    if bestAction[0] != None:
        bestAction[0][-1]["movable"] = False
        v.networkChanges.extend(bestAction[0])
        #v.networkChanges.append({"type": "movable", "unid": c.unid, "movable": False})
        for e in bestAction[0]:
            if e["type"] == "move":
                board[ai_invertCoords(e["position"])[1]][ai_invertCoords(e["position"])[0]] = ""
            if e["type"] == "damage":
                if "kill" in e.keys():
                    for y in range(3):
                        for x in range(4):
                            if board[y][x] != "" and board[y][x].unid == e["target"]:
                                board[y][x] = ""
            

def ai_invertCoords(pos):
    return (3 - pos[0], pos[1])