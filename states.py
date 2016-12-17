import pygame as py
import variables as v
import menuItems
import network
import gameItems
import guiItems
import sys
from renderer import *

def boot():
    """Sets up the game and starts the mainMenu state"""
    py.init()
    v.display = py.display.set_mode((640, 360))
    v.screen = py.Surface((1280, 720))
    py.display.set_caption("Aiopa Battles")
    icon = py.image.load("assets/images/icons/icon.ico")
    py.display.set_icon(icon)
    v.clock = py.time.Clock()
    #mainMenu()
    logo()

def mainMenu():
    """The main menu state"""
    buttons = py.sprite.Group()
    buttons.add(menuItems.Button("Play", (640, 360), 120, (0, 100, 200), (0, 50, 255), "assets/fonts/Galdeano.ttf", "play", centred=True))
    change(py.Rect(0, 0, 1280, 720))
    while True:
        py.event.pump()
        v.events = []
        v.events = py.event.get()
        v.clock.tick(30)
        
        v.screen.fill((0, 255, 255))
        
        for event in v.events:
            if event.type == py.QUIT:
                v.networkHalt = True
                sys.exit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_k:
                    raise Exception("Purposefully Crashed")
        
        buttons.update()
        
        for button in buttons:
            if button.ID == "play":
                if button.pressed():
                    #queue()
                    setup()
                    #game()
                
        refresh()

def setup():
    """The state for setting your name and choosing a deck"""
    name = menuItems.textInput((640, 360), 60, 10, "assets/fonts/Galdeano.ttf", default=["b", "o", "b"], background=(255, 255, 255), centred=True)
    texts = py.sprite.Group()
    texts.add(menuItems.Text("Enter a name", (640, 280), (0, 0, 0), "assets/fonts/Galdeano.ttf", 80, centred=True))
    next = menuItems.Button("Join Queue", (640, 500), 80, (100, 150, 200), (150, 200, 255), "assets/fonts/Galdeano.ttf", "next", centred=True)
    
    change(py.Rect(0, 0, 1280, 720))
    while True:
        v.clock.tick(30)
        py.event.pump()
        v.events = []
        v.events = py.event.get()
        
        for event in v.events:
            if event.type == py.QUIT:
                sys.exit()
        
        v.screen.fill((50, 100, 200))
        
        name.update()
        texts.update()
        next.update()
        
        if next.pressed():
            v.name = name.outText
            queue()
        
        refresh()

def queue():
    """The queue state"""
    loading = menuItems.Text("Joining Queue", (640, 360), (150, 50, 50), "assets/fonts/Galdeano.ttf", 80, centred=True)
    v.screen.fill((50, 100, 200))
    loading.update()
    change(py.Rect(0, 0, 1280, 720))
    refresh()
    py.time.set_timer(py.USEREVENT, 1000) #dot dot dot
    
    skip = menuItems.Button("Skip Queue", (640, 500), 120, (0, 100, 200), (0, 50, 255), "assets/fonts/Galdeano.ttf", "skip", centred=True)
    
    network.queue(loading)
    while True:
        py.event.pump()
        v.events = []
        v.events = py.event.get()
        v.clock.tick(30)
        
        
        v.screen.fill((50, 100, 200))
        for event in v.events:
            if event.type == py.USEREVENT:
                loading.text = loading.text + "."
                if loading.text[-4:] == "....":
                    loading.text = loading.text[:-4]
            if event.type == py.QUIT:
                v.networkHalt = True
                sys.exit()
        if v.game != None:
            v.serverConnected = True
            game()
            
        skip.update()
        if skip.pressed():
            v.networkHalt = True
            game()
            return
        loading.update()
        refresh()
        
def game():
    """The game state"""
    network.getCards()
    network.gameJoin()
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
    for i in range(3):
        gameItems.add_card(v.deck[i], i)
    v.deck = v.deck[3:]
    
    v.gameDeck = py.sprite.OrderedUpdates()
    for i in range(len(v.deck)):
        v.gameDeck.add(gameItems.blankCard(i))
    
    debug = guiItems.debug()
    castles = py.sprite.Group()
    castles.add(gameItems.castle(True))
    castles.add(gameItems.castle(False))
    fade = guiItems.blackFade(100, 10)
    
    coinScreen = guiItems.coinScreen()
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
    
    network.gameLoop()
    
    change(py.Rect(0, 0, 1280, 720))
    
    winEffect = None
        
    while True:
        py.event.pump()
        v.events = []
        v.events = py.event.get()
        if v.debug and py.key.get_pressed()[py.K_SPACE]:
            v.clock.tick(10)
        else:
            v.clock.tick(60)
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
            finish()
            return
        
        network.changes()
        
        
        if not v.pause:
            v.tiles.update()
            v.gameCards.update()
            v.gameDeck.update()
            castles.update()
            turnButton.update()
            turnText.update()
            
            opName.text = v.opName
            opName.update()
            pName.text = v.name
            pName.update()
            v.effects.update()
            gui.update()
            
            if v.pHealth <= 0:
                v.winner = v.opUnid
            if v.opHealth <= 0:
                v.winner = v.unid
                
            if v.winner != None:
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
                if card.intro == True:
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
        
        debug.update()
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
    
    change(py.Rect(0, 0, 1280, 720))
    
    while True:
        py.event.pump()
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
                    mainMenu()
                    return
        refresh()

def crash(crash):
    py.init()
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
            
    change(py.Rect(0, 0, 1280, 720))
    while True:
        py.event.pump()
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
        
def logo():
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
        py.event.pump()
        v.screen.fill((0, 0, 0))
        change(py.Rect(0, 0, 1280, 720))

        if cycle < 25:
            l1pos[0] += 14
        if cycle > 20 and cycle < 45:
            l2pos[0] -= 22
        
        if cycle > 25 and cycle < 225:
            l1pos[0] += 0.1
        if cycle > 45 and cycle < 250:
            l2pos[0] -= 0.1
        
        if cycle > 225:
            l1pos[0] += 40
        if cycle > 240:
            l2pos[0] -= 40
        
        if cycle == 45:
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
            mainMenu()
            return
        
        v.screen.blit(l1, l1pos)
        v.screen.blit(l2, l2pos)
        
        if cycle > 50 and cycle < 60:
            flashAlpha += 25.5
            flash.set_alpha(flashAlpha)
            v.screen.blit(flash, (0, 0))
        if cycle > 55 and cycle < 200:
            flashAlpha -= 1.7
            flash.set_alpha(flashAlpha)
            v.screen.blit(flash, (0, 0))
        
        if cycle > 60 and cycle < 200:
            v.screen.blit(logo, (485, 205))
            
        cycle += 1
        refresh()