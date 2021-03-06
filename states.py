import pygame as py
import variables as v
import menuItems
import network
import gameItems
import guiItems
import campaignAI
import sys
from renderer import *
import tween
import random
from functools import wraps
from webbrowser import open as wbopen
import ctypes

def boot():
    """Sets up the game and starts the mainMenu state"""
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    py.init()
    network.loadMetadata()
    updateDisplay()
    v.screen = py.Surface((1280, 720))
    py.display.set_caption("Aiopa Battles")
    icon = py.image.load("assets/images/icons/icon4.png")
    py.display.set_icon(icon)
    v.clock = py.time.Clock()
    py.key.set_repeat(200, 70)
    v.state = logo if not v.debug else login
    while True:
        change(py.Rect(0, 0, 1280, 720))
        v.state()
    

def mainMenu():
    """The main menu state"""
    buttons = py.sprite.Group()
    if v.loggedIn: 
        buttons.add(menuItems.Button("Play Online", (640, 400), 80, (0, 100, 150), (20, 50, 100), "assets/fonts/Galdeano.ttf", "play", centred=True, bsize=(400, 100)))
        buttons.add(menuItems.Button("Account", (745, 630), 50, (0, 100, 150), (20, 50, 100), "assets/fonts/Galdeano.ttf", "account", centred=True, bsize=(190, 80)))
    else:
        buttons.add(menuItems.Button("Play Online", (640, 400), 80, (100, 100, 100), (100, 100, 100), "assets/fonts/Galdeano.ttf", "-play", centred=True, bsize=(400, 100)))
        buttons.add(menuItems.Button("Account", (745, 630), 50, (100, 100, 100), (100, 100, 100), "assets/fonts/Galdeano.ttf", "-account", centred=True, bsize=(190, 80)))
    buttons.add(menuItems.Button("Test Run", (1000, 400), 40, (0, 100, 150), (20, 50, 100), "assets/fonts/Galdeano.ttf", "test", centred=True, bsize=(150, 40)))
    buttons.add(menuItems.Button("Campaign", (640, 520), 80, (0, 100, 150), (20, 50, 100), "assets/fonts/Galdeano.ttf", "camp", centred=True, bsize=(400, 100)))
    buttons.add(menuItems.Button("Options", (535, 630), 50, (0, 100, 150), (20, 50, 100), "assets/fonts/Galdeano.ttf", "options", centred=True, bsize=(190, 80)))
    buttons.add(menuItems.ImageButton("assets/images/github.png", (1220, 660), (80, 80), (90, 60, 180), "github", centred=True))
    
    background = menuItems.StarBackground()
    black = guiItems.blackFade()
    black.alpha = 255
    
    title = py.sprite.Group()
    title.add(menuItems.Text("Aiopa", (640, 130), (220, 220, 220), "assets/fonts/BlackChancery.ttf", 160, centred=True))
    title.add(menuItems.Text("Battles)", (640, 260), (220, 220, 220), "assets/fonts/Barbarian.ttf", 100, centred=True))
    
    texts = py.sprite.Group()
    texts.add(menuItems.Text("Version " + str(v.version), (20, 680), (240, 220, 220), "assets/fonts/Galdeano.ttf", 20, centred=False))
    black2 = guiItems.blackFade()
    out = None
    
    while True:
        v.events = []
        v.events = py.event.get()
        v.clock.tick(30)
        background.update()        
        for event in v.events:
            if event.type == py.QUIT:
                v.networkHalt = True
                sys.exit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_k:
                    raise Exception("Purposefully Crashed")
        
        buttons.update()
        texts.update()
        for button in buttons:
            if button.pressed():
                if button.ID == "play":
                    out = "play"
                if button.ID == "camp":
                    out = "camp"
                if button.ID == "test":
                    v.test = True
                    v.online = False
                    v.state = game
                    return
                if button.ID == "options":
                    out = "options"
                if button.ID == "github":
                    wbopen("https://github.com/lightopa/Aiopa-Battles")
        
        black.fadeOut()
        title.update()
        if out != None:
            black2.fadeIn()
            if black2.alpha >= 255:
                if out == "play":
                    v.state = queue
                    return
                if out == "camp":
                    v.state = campaign
                    return
                if out == "options":
                    v.state = options
                    return
        refresh()

def options():
    buttons = py.sprite.Group()
    buttons.add(menuItems.Button("Back", (120, 660), 60, (0, 100, 150), (20, 50, 100), "assets/fonts/Galdeano.ttf", "back", bsize=(200, 80), centred=True))
    buttons.add(menuItems.Button("Apply", (1160, 660), 60, (0, 100, 150), (20, 50, 100), "assets/fonts/Galdeano.ttf", "apply", bsize=(200, 80), centred=True))
    
    ops = py.sprite.Group()
    ops.add(menuItems.Option((50, 50), "Fullscreen", ["True", "False"], 80, "full", type="switch", selected=str(v.fullscreen), disabled=False))
    ops.add(menuItems.Option((50, 150), "Debug Info", ["True", "False"], 80, "debug", type="switch", selected=str(v.debug), disabled=False))
    ops.add(menuItems.Option((50, 250), "Ping Frequency", ["100ms", "300ms", "500ms", "700ms", "1000ms"], 80, "ping", type="dropdown", selected=str(int(v.pingFreq * 1000)) + "ms", disabled=False))
    
    infos = py.sprite.Group()
    infos.add(menuItems.InfoBubble((700, 90), "Toggle if the game is in fullscreen mode", "right", 40, (240, 200, 220), 35, target="i"))
    infos.add(menuItems.InfoBubble((730, 190), "Toggle the display of debug information in the top left corner", "right", 40, (240, 200, 220), 30, target="i"))
    infos.add(menuItems.InfoBubble((770, 290), "The rate at which moves are pushed/fetched from the server. A lower time frequency will decrease fps on some systems", "right", 40, (240, 200, 220), 30, target="i"))
    background = menuItems.StarBackground(direction=2, speedmod=0.5, stars=200)
    
    black = guiItems.blackFade()
    black.alpha = 255
    
    black2 = guiItems.blackFade()
    out = None
    
    while True:
        v.clock.tick(30)
        v.events = []
        v.events = py.event.get()
        
        for event in v.events:
            if event.type == py.QUIT:
                sys.exit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_F11:
                    for op in ops:
                        if op.ID == "full":
                            op.selected = str(not v.fullscreen)
        
        for button in buttons:
            if button.pressed():
                if button.ID == "apply":
                    for op in ops:
                        if op.ID == "full":
                            v.fullscreen = op.selected == "True"
                        if op.ID == "debug":
                            v.debug = op.selected == "True"
                        if op.ID == "ping":
                            v.pingFreq = int(op.selected.strip("ms")) / 1000
                    updateDisplay()
                    network.saveMetadata()
                if button.ID == "back":
                    out = "back"
        
        background.update()
                
        buttons.update()
        ops.update()
        infos.update()
        
        black.fadeOut()
        if out != None:
            black2.fadeIn()
            if black2.alpha >= 255:
                if out == "back":
                    v.state = mainMenu
                    return
        refresh()

def setup():
    """The state for setting your name and choosing a deck"""
    texts = py.sprite.Group()
    texts.add(menuItems.Text("Enter a name", (640, 280), (0, 0, 0), "assets/fonts/Galdeano.ttf", 80, centred=True))
    next = menuItems.Button("Join Queue", (640, 500), 80, (100, 150, 200), (150, 200, 255), "assets/fonts/Galdeano.ttf", "next", centred=True)
    
    while True:
        v.clock.tick(30)
        v.events = []
        v.events = py.event.get()
        
        for event in v.events:
            if event.type == py.QUIT:
                sys.exit()
        
        v.screen.fill((50, 100, 200))
        
        texts.update()
        next.update()
        
        if next.pressed():
            v.state = queue
            return
        
        refresh()

def queue():
    """The queue state"""
    loading = menuItems.Text("Joining Queue", (640, 540), (200, 200, 200), "assets/fonts/Galdeano.ttf", 80, centred=True)
    py.time.set_timer(py.USEREVENT, 1000) #dot dot dot
        
    network.queue(loading)
    
    loadingC = menuItems.LoadingCircle(300, pos=(640, 360))
    
    background = menuItems.StarBackground(direction=1, speedmod=5, stars=500)
    
    black = guiItems.blackFade()
    black.alpha = 255
    while True:
        v.events = []
        v.events = py.event.get()
        v.clock.tick(30)
        
        background.update()
        loadingC.update()
        for event in v.events:
            if event.type == py.USEREVENT:
                loading.text = loading.text + "."
                if loading.text[-4:] == "....":
                    loading.text = loading.text[:-4]
            if event.type == py.QUIT:
                v.networkHalt = True
                sys.exit()
        if v.game != None:
            v.online = True
            v.state = game
            return
        loading.update()
        black.fadeOut()
        refresh()

def campaign():
    background = py.image.load("assets/images/map/map_base.png").convert_alpha()
    background2 = py.image.load("assets/images/map/map_top.png").convert_alpha()
    
    v.mapFlags = py.sprite.Group()
    for num in range(1):
        v.mapFlags.add(menuItems.MapFlag((350, 530), num))
        
    black1 = guiItems.blackFade()
    black1.alpha = 255
    
    black2 = guiItems.blackFade(limit=150, gradient=True)
    
    v.leaveMap = False
    
    while True:
        v.events = []
        v.events = py.event.get()
        v.clock.tick(60)
        
        v.screen.fill((153, 102, 51))
        v.screen.blit(background, (0, 0))
        v.screen.blit(background2, (0, 0))
        v.mapFlags.update()
        
        if v.levelDescription != None:
            black2.fadeIn()
            v.levelDescription.update()
        else:
            black2.fadeOut()
        
        if v.leaveMap == False:
            black1.fadeOut()
        else:
            black1.fadeIn()
            if black1.alpha >= 255:
                v.state = aiSetup
                return
        refresh()

def aiSetup():
    v.online = False
    v.opUnid = 0
    v.unid = 1
    v.opName = v.levels[v.selectedLevel]["opName"]
    if v.levels[v.selectedLevel]["pStart"]:
        v.gameStarter = v.unid
    else:
        v.gameStarter = v.opUnid
    
    v.gameTurn = {"player": v.gameStarter, "time": 0}
    
    v.opDeck = list(v.cards.values())
    v.opHand = v.opDeck[:3]
    v.opDeck = v.opDeck[3:]
    v.opMana = 0
    v.state = game

def game():
    """The game state"""
    if v.online:
        network.getCards()
        network.gameJoin()
    elif v.test:
        v.gameStarter = v.unid
        v.gameTurn = {"player": v.unid, "time": 0}
        v.opUnid = 1
        v.opName = "Test"
    background = py.image.load("assets/images/paper.png").convert()
    background = py.transform.scale(background, (1280, 720))
    v.tiles = py.sprite.Group()
    for y in range(0, 3):
        for x in range(0, 4):
            v.tiles.add(gameItems.tile((x, y), "board"))
    
    pcstl = gameItems.tile((-1, 0), "board", True)
    v.tiles.add(pcstl)
    opcstl = gameItems.tile((4, 0), "board", False)
    v.tiles.add(opcstl)

    v.gameCards = py.sprite.Group()
    v.deck = list(v.cards.values())
    v.hand = []
    for i in range(3):
        v.hand.append(gameItems.add_card(v.deck[i], i))
    v.deck = v.deck[3:]
    
    v.gameDeck = py.sprite.OrderedUpdates()
    for i in range(len(v.deck)):
        v.gameDeck.add(gameItems.blankCard(i))
    
    castles = py.sprite.Group()
    castles.add(gameItems.castle(True))
    castles.add(gameItems.castle(False))
    fade = guiItems.blackFade(100, 10)
    
    coinScreen = guiItems.coinScreen()
    if not v.test:
        v.pause = True
        v.pauseType = "coin"
    
    turnButton = menuItems.Button("End Turn", (1100, 630), 40, (250, 250, 230), (230, 230, 200), "assets/fonts/Galdeano.ttf", "turn", centred=True, bsize=(150, 150))
    turnText = menuItems.Text("", (1100, 530), (0, 0, 0), "assets/fonts/Galdeano.ttf", 40, True)
    opName = menuItems.Text("", (1100, 40), (0, 0, 0), "assets/fonts/Galdeano.ttf", 40, True)
    pName = menuItems.Text("", (180, 40), (0, 0, 0), "assets/fonts/Galdeano.ttf", 40, True)
    
    gui = py.sprite.Group()
    gui.add(guiItems.healthBar(True))
    gui.add(guiItems.healthBar(False))
    gui.add(guiItems.timer())
    gui.add(guiItems.ManaMeter())
    v.pturn = guiItems.PlayerTurn()
    
    v.effects = py.sprite.Group()
    if v.online:
        network.gameLoop()
        
    winEffect = None
    
    changeCount = 0
        
    while True:
        v.events = []
        v.events = py.event.get()
        if v.debug and py.key.get_pressed()[py.K_SPACE]:
            v.clock.tick(10)
        elif not v.test:
            v.clock.tick(60)
        else:
            v.clock.tick()
        v.hoverTile = None
        v.screen.blit(background, (0, 0))
        
        for event in v.events:
            if event.type == py.QUIT:
                v.networkHalt = True
                network.gameLeave()
                sys.exit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_d:
                    v.debug = True
                if event.key == py.K_k:
                    raise Exception("Purposefully Crashed")
        if v.gameStop != None:
            v.state = finish
            return
        
        if v.online or (changeCount % 40 == 0):
            network.changes()
        changeCount += 1
        
        
        if not v.pause:
            v.tiles.update()
            v.gameCards.update()
            v.gameDeck.update()
            castles.update()
            turnButton.update()
            turnText.update()
            
            opName.text = v.opName
            opName.update()
            pName.text = v.username
            pName.update()
            v.effects.update()
            gui.update()
            
            if v.pHealth <= 0: # Opponent wins
                if v.winner == None and v.online:
                    v.account["competitive"] = 20
                    cpMult = v.account["competitive"] / v.opAccount["competitive"]
                    cpAdd = int(cpMult * -10)
                    if cpAdd > -5:
                        cpAdd = -5
                    if v.account["competitive"] + cpAdd <= 0:
                        cpAdd = -v.account["competitive"] + 1
                    network.updateAccount({"losses": 1, "competitive": cpAdd})
                v.winner = v.opUnid
            
            if v.opHealth <= 0: # Player wins
                if v.winner == None and v.online:
                    cpMult = v.opAccount["competitive"] / v.account["competitive"]
                    cpAdd = int(cpMult * 10)
                    if cpAdd < 2:
                        cpAdd = 2
                    network.updateAccount({"wins": 1, "competitive": cpAdd})
                v.winner = v.unid
                
            if v.winner != None:
                v.networkHalt = True
                if v.online:
                    v.comp = (v.account["competitive"], cpAdd)
                if winEffect == None:
                    if v.winner == v.opUnid:
                        t = pcstl
                    else:
                        t = opcstl
                    winEffect = gameItems.Effect("explosion", target=t, sheet="assets/images/effects/explosion1.png")
                elif winEffect.alive() == False:
                    v.pause = True
                    v.pauseType = "win"
                    winScreen = guiItems.endScreen()
            
            if v.dragCard != None:
                fade.fadeIn()
                for tile in v.availableTiles:
                    tile.draw()
                    for card in v.gameCards:
                        if card.tile == tile:
                            card.draw()
                v.dragCard.draw()
            else:
                fade.fadeOut()
                
            for card in v.gameCards:
                if card.type == "minion" and card.attackTarget != None:
                    card.draw()
                if card.intro == True or (card.card.type == "minion" and card.opintro == True):
                    card.draw()
            
            v.pturn.update()
            
            if coinScreen.state == "out":
                coinScreen.black.fadeOut() 
                
            if turnButton.pressed():
                if v.gameTurn["player"] == v.unid:
                    v.networkEvents.append({"type": "turn"})
                    v.gameTurn["player"] = None
            
            
            if v.gameTurn["player"] == v.unid:
                turnText.text = "Your Turn"
            else:
                turnText.text = "Opponent's Turn"
                
                
            if v.timeLeft <= 0 and v.gameTurn["player"] == v.unid:
                v.networkEvents.append({"type": "turn"})
                v.gameTurn["player"] = None
            
            
        if v.pause:
            for s in v.tiles:
                s.draw()
            for s in v.gameCards:
                s.draw()
            for s in v.gameDeck:
                s.draw()
            for s in castles:
                s.draw()
            for s in v.effects:
                s.draw()
            for s in gui:
                s.draw()
            turnButton.draw()
            turnText.draw()
            opName.draw()
            pName.draw()
            v.pturn.draw()
            if v.pauseType == "coin":
                coinScreen.update()
                
            if v.pauseType == "win":
                winScreen.update()
                
        if v.online == False and not v.test:
            campaignAI.ai()
        
        refresh()

def finish():
    """The state that is run after a game has ended"""
    buttons = py.sprite.Group()
    buttons.add(menuItems.Button("Return to main menu", (640, 500), 80, (100, 150, 200), (150, 200, 255), "assets/fonts/Galdeano.ttf", "title", centred=True))
    
    texts = py.sprite.Group()
    if v.gameStop == "disconnect":
        texts.add(menuItems.Text("Your opponent disconnected", (640, 360), (255, 255, 255), "assets/fonts/Galdeano.ttf", 60, True))
    if v.gameStop == "timeout":
        texts.add(menuItems.Text("Your opponent timed out", (640, 360), (255, 255, 255), "assets/fonts/Galdeano.ttf", 60, True))
    if v.gameStop == "bad":
        texts.add(menuItems.Text("Bad input from server (view logs)", (640, 360), (255, 255, 255), "assets/fonts/Galdeano.ttf", 60, True))
    if v.gameStop == "missing":
        texts.add(menuItems.Text("The server misplaced the current game data", (640, 360), (255, 255, 255), "assets/fonts/Galdeano.ttf", 60, True))
        
    while True:
        v.screen.fill((50, 100, 200))
        v.events = []
        v.events = py.event.get()
        
        for event in v.events:
            if event.type == py.QUIT:
                sys.exit()
        
        buttons.update()
        texts.update()
        
        for button in buttons:
            if button.ID == "title":
                if button.pressed():
                    v.state = mainMenu
                    return
        refresh()

def crash(crash):
    """The state that displays a crash report"""
    texts = py.sprite.Group()
    buttons = py.sprite.Group()
    buttons.add(menuItems.Button("Copy to Clipboard", (40, 650), 40, (50, 255, 50), (0, 200, 0), None, "copy"))
    buttons.add(menuItems.Button("Upload Report", (440, 650), 40, (50, 255, 50), (0, 200, 0), None, "upload"))
    buttons.add(menuItems.Button("Exit", (840, 650), 40, (50, 255, 50), (0, 200, 0), None, "quit"))
    
    posy = 70
    import os.path
    parent = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    parent = parent.replace("\\", "/")
    for line in crash.split("\n"):
        out = line.strip("\n")
        out = out.replace("\\", "/")
        out = out.split(parent)
        out = "".join(out)
        out = out.replace("  ", "    ")
        texts.add(menuItems.Text(out, (60, posy), (0, 0, 0), None, 30))
        posy += 32
            
    while True:
        v.events = []
        v.events = py.event.get()
        v.screen.fill((50, 0, 255))
        py.draw.rect(v.screen, (255, 255, 255), (40, 40, 1200, 600))
        py.draw.rect(v.screen, (0, 0, 0), (40, 40, 1200, 600), 2)
        texts.update()
        buttons.update()
        for button in buttons:
            if button.pressed():
                if button.ID == "upload":
                    pass
                if button.ID == "copy":
                    py.scrap.init()
                    py.scrap.put(py.SCRAP_TEXT, str(crash).encode())
                if button.ID == "quit":
                    return
        for event in v.events:
            if event.type == py.QUIT:
                return
        refresh()

def login():
    """The state that handles logging into an account"""
    buttons = py.sprite.Group()
    buttons.add(menuItems.Button("Login", (640, 550), 50, (255, 100, 100), (200, 150, 150), "assets/fonts/Galdeano.ttf", "login", centred=True, bsize=(200, 50)))
    buttons.add(menuItems.Button("Register", (640, 600), 25, (255, 100, 100), (200, 150, 150), "assets/fonts/Galdeano.ttf", "register", centred=True, bsize=(200, 30)))
    
    network.loadMetadata()
    uname = menuItems.TextBox((640, 400, 200, 50), fontf="assets/fonts/FSB.ttf", size=30, default=v.username)
    pword = menuItems.TextBox((640, 480, 200, 50), fontf="assets/fonts/FSB.ttf", size=30, active=False, replace="*", default=v.password)
    
    title = py.sprite.Group()
    title.add(menuItems.Text("Aiopa", (640, 130), (220, 220, 220), "assets/fonts/BlackChancery.ttf", 160, centred=True))
    title.add(menuItems.Text("Battles)", (640, 260), (220, 220, 220), "assets/fonts/Barbarian.ttf", 100, centred=True))
    
    texts = py.sprite.Group()
    un = menuItems.Text("username", (540, 350), (255, 255, 255), "assets/fonts/Galdeano.ttf", 20, centred=False)
    texts.add(un)
    pw = menuItems.Text("password", (540, 430), (255, 255, 255), "assets/fonts/Galdeano.ttf", 20, centred=False)
    texts.add(pw)
    
    backFire = menuItems.Animation((0, -400, 1280, 1280), "assets/images/menu/fire.png", 50, 1, 60)
    black = guiItems.blackFade()
    black.alpha = 255
    black2 = guiItems.blackFade()
    out = None
    
    loading = menuItems.LoadingCircle(200, pos=(640, 430))
    loadingText = menuItems.Text("Logging in...", (640, 550), (255, 255, 255), "assets/fonts/Galdeano.ttf", 40, centred=True)
    offlineButton = menuItems.Button("Play Offline", (640, 620), 40, (240, 240, 240), (230, 255, 255), "assets/fonts/Galdeano.ttf", "offline", centred=True, bsize=(220, 80))
    
    wait = 0
    while True:
        v.events = []
        v.events = py.event.get()
        v.clock.tick(60)
        change(py.Rect(0, 0, 1280, 720))
        for button in buttons:
            if button.pressed():
                if button.ID == "login":
                    out = "log"
                    network.login(uname.final, pword.final)
                if button.ID == "register":
                    out = "reg"
        backFire.update()
        buttons.update()
        tween.update()
        uname.update()
        pword.update()
        texts.update()
        if out != None:
            black2.fadeIn()
            if black2.alpha >= 255:
                if out == "reg":
                    v.state = register
                    return
                if out == "log":
                    loading.update()
                    loadingText.update()
                    if v.timeoutStage == 1:
                        loadingText.text = "Taking longer than expected..."
                    if v.timeoutStage == 2:
                        loadingText.text = "Can't connect to server"
                        offlineButton.update()
                        if offlineButton.pressed():
                            v.username = uname.final
                            v.password = pword.final
                            network.saveMetadata()
                            v.loggedIn = False
                            v.state = mainMenu
                            return
                    wait += 1
                    if v.loggedIn != False and wait > 100:
                        if v.loggedIn == True:
                            v.username = uname.final
                            v.password = pword.final
                            network.saveMetadata()
                            v.state = mainMenu
                            return
                        elif v.loggedIn == "username":
                            un.text = "username doesn't exist"
                            uname.colour = (255, 0, 0)
                            pword.colour = (255, 255, 255)
                        elif v.loggedIn == "password":
                            un.text = "Incorrect password"
                            uname.colour = (255, 255, 255)
                            pword.colour = (255, 0, 0)
                        v.loggedIn = False
                        out = None
        else:
            black2.fadeOut()
                
        title.update()
        black.fadeOut()
        refresh()
        
def register():
    """The state that handles registering a new account"""
    buttons = py.sprite.Group()
    buttons.add(menuItems.Button("Register", (640, 550), 50, (255, 100, 100), (200, 150, 150), "assets/fonts/Galdeano.ttf", "register", centred=True, bsize=(200, 50)))
    
    uname = menuItems.TextBox((640, 400, 200, 50), fontf="assets/fonts/FSB.ttf", size=30)
    pword1 = menuItems.TextBox((520, 480, 200, 50), fontf="assets/fonts/FSB.ttf", size=30, active=False, replace="*")
    pword2 = menuItems.TextBox((760, 480, 200, 50), fontf="assets/fonts/FSB.ttf", size=30, active=False, replace="*")
    
    title = py.sprite.Group()
    title.add(menuItems.Text("Aiopa", (640, 130), (220, 220, 220), "assets/fonts/BlackChancery.ttf", 160, centred=True))
    title.add(menuItems.Text("Battles)", (640, 260), (220, 220, 220), "assets/fonts/Barbarian.ttf", 100, centred=True))
    
    texts = py.sprite.Group()
    un = menuItems.Text("username", (540, 350), (255, 255, 255), "assets/fonts/Galdeano.ttf", 20, centred=False)
    texts.add(un)
    texts.add(menuItems.Text("password", (420, 430), (255, 255, 255), "assets/fonts/Galdeano.ttf", 20, centred=False))
    texts.add(menuItems.Text("re-enter password", (660, 430), (255, 255, 255), "assets/fonts/Galdeano.ttf", 20, centred=False))
    
    backFire = menuItems.Animation((0, -400, 1280, 1280), "assets/images/menu/sparks.png", 33, 1, 80)
    black = guiItems.blackFade()
    black.alpha = 255
    black2 = guiItems.blackFade()
    out = None
    
    loading = menuItems.LoadingCircle(200)
    loadingText = menuItems.Text("Registering Account...", (640, 480), (255, 255, 255), "assets/fonts/Galdeano.ttf", 40, centred=True)
    wait = 0
    while True:
        v.events = []
        v.events = py.event.get()
        v.clock.tick(60)
        change(py.Rect(0, 0, 1280, 720))
        for button in buttons:
            if button.pressed():
                if button.ID == "register":
                    if uname.final == "":
                        uname.colour = (255, 0, 0)
                    elif pword1.final == "":
                        uname.colour = (255, 255, 255)
                        pword1.colour = (255, 0, 0)
                    elif pword1.final != pword2.final:
                        uname.colour = (255, 255, 255)
                        pword1.colour = (255, 255, 255)
                        pword2.colour = (255, 0, 0)
                    else:
                        out = "reg"
                        network.registerAccount(uname.final, pword1.final)
                        wait = 0
        backFire.update()
        buttons.update()
        tween.update()
        uname.update()
        pword1.update()
        pword2.update()
        texts.update()
        black.fadeOut()
        title.update()
        if out == "reg":
            black2.fadeIn()
            if black2.alpha >= 255:
                loading.update()
                loadingText.update()
                if v.registerSuccess != None:
                    if v.registerSuccess:
                        loadingText.text = "Account Created!"
                        wait += 1
                        if wait >= 80:
                            v.username = uname.final
                            v.password = pword1.final
                            network.saveMetadata()
                            v.state = login
                            return
                    else:
                        loadingText.text = "Username Already Exists"
                        un.text = "username already exists"
                        uname.colour = (255, 0, 0)
                        wait += 1
                        if wait >= 80:
                            out = None
                            loadingText.text = "Registering Account..."
        else:
            black2.fadeOut()
                        
        refresh()
        
def logo():
    """The state that plays the logo animation"""
    font = py.font.Font("assets/fonts/slant.ttf", 100)
    l1 = font.render("Lightopa", 1, (0, 255, 255))
    font = py.font.Font("assets/fonts/slant.ttf", 120)
    l2 = font.render("Games", 1, (0, 255, 255))
    logo = py.image.load("assets/images/logo.png").convert_alpha()
    logo = py.transform.scale(logo, (310, 310))
    
    l1pos = [-200, 200]
    l2pos = [1280, 380]
    flash = py.Surface((1280, 720))
    flash.fill((255, 255, 255))
    flash.set_alpha(0)
    flashAlpha = 0
    
    cycle = 0
    
    v.clock = py.time.Clock()
    
    py.mixer.init()
    thunder = py.mixer.Sound("assets/sounds/Thunder.ogg")
    thunder.set_volume(0.2)
    
    while True:
        v.clock.tick(60)
        v.screen.fill((0, 0, 0))
        change(py.Rect(0, 0, 1280, 720))

        if cycle < 20:
            l1pos[0] += 32 - (32 * cycle / 20)
        if cycle > 10 and cycle < 30:
            l2pos[0] -= 58 - (58 * (cycle - 10) / 20)
        
        if cycle > 19 and cycle < 225:
            l1pos[0] += 0.1
        if cycle > 29 and cycle < 250:
            l2pos[0] -= 0.1
        
        if cycle > 225:
            l1pos[0] += (40 * (cycle - 225) / 20)
        if cycle > 240:
            l2pos[0] -= (40 * (cycle - 225) / 20)
        
        if cycle == 30:
            thunder.play()
        
        if cycle >= 200 and cycle < 250:
            v.screen.blit(logo, (485, 205))
            
        
        if cycle > 250 and cycle < 300:
            size = int(1.5 * (cycle - 250)**2 + 310)
            l = py.transform.scale(logo, (size, size))
            v.screen.blit(l, (640 - size/2, 360 - size/2))
        if cycle > 250 and cycle < 300:
            flashAlpha += 6
            flash.set_alpha(flashAlpha)
            v.screen.blit(flash, (0, 0))
        if cycle >= 300:
            flashAlpha -= 8
            flash.set_alpha(flashAlpha)
            v.screen.blit(flash, (0, 0))
        if cycle > 340:
            v.state = login
            return
        
        v.screen.blit(l1, l1pos)
        v.screen.blit(l2, l2pos)
        
        if cycle > 30 and cycle < 40:
            flashAlpha += 25.5
            flash.set_alpha(flashAlpha)
            v.screen.blit(flash, (0, 0))
        if cycle > 35 and cycle < 200:
            flashAlpha -= 1.7
            flash.set_alpha(flashAlpha)
            v.screen.blit(flash, (0, 0))
        
        if cycle > 40 and cycle < 200:
            v.screen.blit(logo, (485, 205))
            
        cycle += 1
        refresh()