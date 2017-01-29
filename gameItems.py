import pygame as py
import variables as v
import random
from renderer import change
import pathfind

class SpriteSheet():
    def __init__(self, file_name, rows, columns):
        """Takes an image and splits it into multiple images.
        
        Args:
            file_name (str/pygame.Surface): The image to split.
            rows (int): The number of rows the sprite sheet has.
            columns (int): The number of columns the sprite sheet has.
        """

        self.rows = rows
        self.columns = columns

        # Load the sprite sheet.
        if type(file_name) is py.Surface:
            self.sprite_sheet = file_name.convert_alpha()
        else:
            self.sprite_sheet = py.image.load(file_name).convert_alpha()
        self.getGrid()

    def getGrid(self):
        """Generates a list of images from the sprite sheet"""
        width = self.sprite_sheet.get_size()[0] / self.columns
        height = self.sprite_sheet.get_size()[1] / self.rows
        all = []
        for h in range(self.rows):
            for w in range(self.columns):
                image = py.Surface([width, height], py.SRCALPHA, 32).convert_alpha()
                image.blit(self.sprite_sheet, (0, 0), (w * width, h * height, width, height))
                all.append(image)
        self.images = all

def add_card(card, order=0, **kwargs):
    if card.type == "minion":
        out = minionCard(card, order, **kwargs)
        v.gameCards.add(out)
    if card.type == "spell":
        out = spellCard(card, order, **kwargs)
        v.gameCards.add(out)
    return out
    
class tile(py.sprite.Sprite):
    def __init__(self, pos, style, castle=None):
        """Creates a single game tile.
        
        Tiles are arranged in a grid, and can have cards placed on them.
        
        Args:
            pos x,y ((int, int)): The tile number in the x and y directions.
            style (str): The style id to use.
        """
        super().__init__()
        sheet = SpriteSheet("assets/images/tiles.png", 6, 5)
        size = 150
        
        if castle == None:
            self.border = py.Surface((size, size), py.SRCALPHA, 32).convert_alpha()
            py.draw.rect(self.border, (255, 255, 255), (0, 0, size, size), 3)
            if style == "grass":
                self.image = sheet.images[random.choice([0, 5])]
                self.border.fill((200, 255, 200, 50), special_flags=py.BLEND_RGBA_ADD)
            if style == "board":
                self.image = py.Surface((size, size), py.SRCALPHA, 32)
                self.image.fill((250, 230, 200, 100))
                self.border.fill((150, 130, 100, 150), special_flags=py.BLEND_RGBA_MIN)
        
            self.image = py.transform.scale(self.image, (size, size))
            self.image.blit(self.border, (0, 0))
            self.rect = py.Rect(((640 - size*2) + pos[0] * size, (280 - size*1.5) + pos[1] * size), (size, size))
            self.rimage = self.image
        else:            
            if castle == True:
                self.image = py.image.load("assets/images/dashesP.png")
                self.rect = py.Rect(40, 55, 300, 450)
            if castle == False:
                self.image = py.image.load("assets/images/dashesE.png")
                self.rect = py.Rect(940, 55, 300, 450)
            self.rimage = py.Surface((0, 0))
        
        self.castle = castle
        self.hovered = False
        
        self.pos = pos
        self.attack = False
        self.card = None
    
    def draw(self):
        change(v.screen.blit(self.rimage, self.rect))
    
    def update(self):
        if self.rect.collidepoint(v.mouse_pos):
            self.hovered = True
        else:
            self.hovered = False
        
        self.attack = False
        
        self.card = None
        for card in v.gameCards:
            if card.tile == self:
                self.card = card
        
        if v.dragCard != None:
            #If card is being dragged
            if v.dragCard.type == "minion":
                #If it is a minion card
                if v.dragCard.tile == None:
                    #If the card is in the player's hand
                    if self.pos[0] < 2:
                        v.availableTiles.add(self)
                else:
                    #If the card is on the board
                    if self.castle == None:
                        #If this tile isn't a castle tile
                        path = pathfind.pathfind(v.dragCard.tile.pos, self.pos, pathfind.get_grid(skip=[]))
                        a = False
                        for card in v.gameCards:
                            if card.tile == self:
                                if card.player == v.opUnid:
                                    a = True
                                    path = pathfind.pathfind(v.dragCard.tile.pos, self.pos, pathfind.get_grid(skip=[self]))
                        if path != False and len(path) - 1 <= v.dragCard.moves and v.dragCard.card.speed > 0:
                            v.availableTiles.add(self)
                            if a:
                                self.attack = True
                        if v.dragCard.moves > 0 and v.dragCard.range > 0 and a and abs(v.dragCard.tile.pos[0] - self.pos[0]) <= v.dragCard.range and abs(v.dragCard.tile.pos[1] - self.pos[1]) <= v.dragCard.range:
                            v.availableTiles.add(self)
                            self.attack = True
                    else:
                        #If this tile is a castle tile
                        if self.castle == False:
                            paths = [pathfind.pathfind((v.dragCard.tile.pos[0] + 1, v.dragCard.tile.pos[1]), (self.pos[0] + 1, 0), pathfind.get_grid(skip=[], castle=True)), 
                                     pathfind.pathfind((v.dragCard.tile.pos[0] + 1, v.dragCard.tile.pos[1]), (self.pos[0] + 1, 1), pathfind.get_grid(skip=[], castle=True)), 
                                     pathfind.pathfind((v.dragCard.tile.pos[0] + 1, v.dragCard.tile.pos[1]), (self.pos[0] + 1, 2), pathfind.get_grid(skip=[], castle=True))]
                            paths = [p for p in paths if p != False]
                            if len(paths) > 0:
                                path = paths[0]
                                for p in paths:
                                    if len(p) < len(path):
                                        path = p
                            else:
                                path = False
                                    
                            if path != False and len(path) - 1 <= v.dragCard.moves and v.dragCard.card.speed > 0:
                                v.availableTiles.add(self)
                                self.attack = True
                        
            if v.dragCard.type == "spell":
                if self.card != None:
                    v.availableTiles.add(self)
                    self.attack = True
                    
                    
                
        if v.availableTiles != None:
            if not self in v.availableTiles:
                self.hovered = False
 
        self.rimage = self.image.copy()
        
        if self.card != None:
            if self.card.player == v.unid:
                self.rimage.fill((100, 255, 100, 200), special_flags=py.BLEND_RGBA_MULT)
            else:
                self.rimage.fill((255, 100, 100, 200), special_flags=py.BLEND_RGBA_MULT)
        
        if self.castle != None:
            if self.attack:
                self.rimage = self.image.copy()
            else:
                self.rimage = py.Surface((0, 0))
        
        if self.hovered:
            v.hoverTile = self
            if self.attack:
                self.rimage.fill((200, 200, 200, 0), special_flags=py.BLEND_RGBA_MAX)
            else:
                self.rimage.fill((255, 255, 255, 200))
            
        self.draw()
            

class card:
    def __init__(self, attributes):
        """A container for information about a single card.
        
        Args:
            attributes (dict): A dictionary of attributes for the card
        """
        self.name = attributes["name"]
        self.type = attributes["type"]
        if self.type == "minion":
            self.attack = attributes["attack"]
            self.health = attributes["health"]
            self.speed = attributes["speed"]
        if self.type == "spell":
            pass
        self.effects = []
        if "effects" in attributes.keys():
            self.effects = attributes["effects"]
        self.description = attributes["description"]
        self.cost = attributes["cost"]
        self.id = attributes["id"]
        
class gameCard(py.sprite.Sprite):
    def __init__(self, cardClass, order=0, unid=None, changes={}, renSize=(155, 220), intro=False):
        """A card that can be placed in the game.
        
        Args:
            cardClass (card): The card class that this object will represent.
            order (int): The position of this card in the player's hand.
        """
        super().__init__()
        self.card = cardClass
        self.type = self.card.type
        self.order = order
        
        self.changes = {"attack": 0,
                        "health": 0,
                        "speed": 0,
                        "cost": 0}
        self.changes.update(changes)
        
        #self.moves = self.card.speed + self.changes["speed"]
        self.moves = 0
        
        if unid == None:
            self.unid = "c" + str(v.unid) + str(v.cardUnid)
            v.cardUnid += 1
        else:
            self.unid = unid
        
        self._render(renSize)

        self.hovered = False
        self.drag = False
        self.cycle = 0
        self.dragPoint = (0, 0)
        
        self.rect = py.Rect((0, 0), (155, 220))
        self.rect.center = (415 + self.order * (self.rect.width + 10), 630)
        
        self.damage = py.image.load("assets/images/damage.png").convert_alpha()
        self.damage = py.transform.scale(self.damage, (100, 100))
        
        self.preCard = []
        self.postCard = []
        
        self.intro = intro
        self.introCycle = 1
    
    def _base_render(self, size):
        if size != None:
            self.size = size
        self.image = py.Surface(self.size)
        icon = py.image.load("assets/images/cards/" + self.card.id + ".png").convert()
        icon = py.transform.smoothscale(icon, (round(600/770 * self.size[0]), round(390/1105 * self.size[1])))
        self.image.blit(icon, (80/770 * self.size[0], 170/1105 * self.size[1]))
        if self.card.type == "minion":
            self.blank = py.image.load("assets/images/cards/blank_minion.png").convert_alpha()
        if self.card.type == "spell":
            self.blank = py.image.load("assets/images/cards/blank_spell.png").convert_alpha()
        self.blank = py.transform.smoothscale(self.blank, (self.size[0], self.size[1]))
        self.image.blit(self.blank, (0, 0))
        
        fs = int(130/770 * self.size[0])
        font = py.font.Font("assets/fonts/Galdeano.ttf", fs)
        render = font.render(str(self.card.cost + self.changes["cost"]), 1, (0, 0, 0))
        self.image.blit(render, (85/770 * self.size[0] - render.get_rect().size[0]/2, 85/1105 * self.size[1] - render.get_rect().size[1]/2))
        
        while font.size(self.card.name)[0] > 420/770 * self.size[0]:
            fs -= 1
            font = py.font.Font("assets/fonts/Galdeano.ttf", fs)
        render = font.render(self.card.name, 1, (0, 0, 0))
        self.image.blit(render, (self.size[0]/2 - render.get_rect().width/2, 90/1105 * self.size[1] - render.get_rect().height/2))
    
    def _render_description(self):
        font = py.font.Font("assets/fonts/Galdeano.ttf", int(80/770 * self.size[0]))
        words = self.card.description.split(" ")
        line = ""
        lineNum = 0
        for word in words:
            fsize = font.size(line + word + " ")
            if fsize[0] < 590/770 * self.size[0]:
                line = line + word + " "
            else:
                render = font.render(line, 1, (0, 0, 0))
                self.image.blit(render, (100/770 * self.size[0], 670/1105 * self.size[1] + lineNum * render.get_rect().height))
                lineNum += 1
                line = word + " "
        render = font.render(line, 1, (0, 0, 0))
        self.image.blit(render, (100/770 * self.size[0], 670/1105 * self.size[1] + lineNum * render.get_rect().height))
        
    def _intro(self):
        pos = (660, 330)
        end = 415 + self.order * 135, 710 - self.rect.size[1]/2
        diff = (end[0] - pos[0], end[1] - pos[1])
        diff = (diff[0]/40, diff[1]/40)
        if self.introCycle >= 40:
            self.intro = False
        pos = (pos[0] + diff[0] * self.introCycle, pos[1] + diff[1] * self.introCycle)
        self.rect.center = pos
        self.rimage = py.transform.scale(self.image, (int(self.rect.size[0] * self.introCycle/40), self.rect.size[1]))
        self.introCycle += 2
    
    def draw(self):
        if self.preCard != []:
            for item in self.preCard:
                change(v.screen.blit(item[0], item[1]))
        change(v.screen.blit(self.rimage, self.rect))
        if self.postCard != []:
            for item in self.postCard:
                change(v.screen.blit(item[0], item[1]))
        
        if self.card.type == "minion" and self.opintro:
            self.blankCard.draw()
        
    
    def _hand_update(self):
        if not self.intro:
            if self.cycle < 30 and self.hovered:
                self.cycle += 4
            if self.cycle > 0 and not self.hovered and not self.drag:
                self.cycle -= 4  
        if self.cycle >= 30:
            self.cycle = 30
        if self.cycle <= 0:
            self.cycle = 0
        
        sMod = 1 + self.cycle/60
        
        self.rect = py.Rect((0, 0), (125 * sMod, 175 * sMod))
        self.rimage = py.transform.scale(self.image, self.rect.size)
        if not self.intro:
            self.rect.center = (415 + self.order * (125 + 10), 710 - self.rect.size[1]/2)
        for card in v.gameCards:
            if card.tile == None and card.cycle > 0:
                if card.order < self.order:
                    self.rect.x += 62 * (1 + card.cycle/60) - 62
                if card.order > self.order:
                    self.rect.x -= 62 * (1 + card.cycle/60) - 62
        
        if self.drag:
            self.rect.x = v.mouse_pos[0] - self.dragPoint[0]
            self.rect.y = v.mouse_pos[1] - self.dragPoint[1]
        
        if self.intro:
            self._intro()
    
    
    def _pre_update(self):
        change(self.rect)
        if self.rect.collidepoint(v.mouse_pos):
            self.hovered = True
        else:
            self.hovered = False
        
        if v.gameTurn != None and v.gameTurn["player"] != v.unid:
            self.drag = False
            v.dragCard = None
            v.availableTiles = None
            self.preCard = []
            self.postCard = []
    
    def update(self):
        self.draw()

class spellCard(gameCard):
    def __init__(self, cardClass, order=0, changes={}, renSize=(155, 220), intro=False):
        """A spell card.
            Args:
            cardClass (card): The card data object for this spell
            order (int): Where the card is in the hand
            changes (dict): Any changes to the card's stats
            renSize (w, h): The size at which to render the card
            intro (bool): Whether or not to play the deck to hand animation
        """
        super().__init__(cardClass, order=order, changes=changes, renSize=renSize, intro=intro)
        self.tile = None
        self._render(renSize)
        self.update()
    
    def _render(self, size=(770, 1105)):
        self._base_render(size)
        self._render_description()
    
    def update(self):
        self._pre_update()
        for event in v.events:
            if v.gameTurn != None and v.gameTurn["player"] == v.unid:
                if self.hovered and event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                    self.drag = True
                    self.dragPoint = (v.mouse_pos[0] - self.rect.x, v.mouse_pos[1] - self.rect.y)
                    v.dragCard = self
                    v.availableTiles = py.sprite.Group()

            if event.type == py.MOUSEBUTTONUP and event.button == 1 and self.drag and v.pMana >= self.card.cost:
                self.drag = False
                v.dragCard = None
                v.availableTiles = None
                self.preCard = []
                self.postCard = []
                if v.hoverTile != None:
                    v.pMana -= self.card.cost
                    target = v.hoverTile.card
                    if "damage" in self.card.effects.keys():
                        target.changes["health"] -= self.card.effects["damage"]
                        v.networkEvents.append({"type": "spell", "effects": self.card.effects, "target": target.unid, "animation": "meteor"})
                        target._render()
                        Effect("meteor", target=v.hoverTile, sheet="assets/images/effects/fireball.png")
                    if not v.debug:
                        self.kill()
                        for card in v.gameCards:
                            if card.tile == None:
                                if card.order > self.order:
                                    card.order -= 1
        self._hand_update()
        self.preCard = []
        if self.drag and v.hoverTile != None:
            self.rect.x = v.hoverTile.rect.x - self.rect.width - 10
            if "damage" in self.card.effects.keys():
                drect = py.Rect(0, 0, 100, 100)
                drect.center = v.hoverTile.rect.center
                self.preCard.append((self.damage, drect))
                font = py.font.Font("assets/fonts/Galdeano.ttf", 30)
                dmg = font.render(str(-self.card.effects["damage"]), 1, (0, 0, 0))
                drect = dmg.get_rect()
                drect.center = v.hoverTile.rect.center
                self.preCard.append((dmg, drect))
        self.draw()

class minionCard(gameCard):
    def __init__(self, cardClass, order=0, tile=None, unid=None, player=None, changes={}, renSize=(155, 220), intro=False, opintro=False):
        """A minion card.
            Args:
            cardClass (card): The card data object for this minion
            order (int): Where the card is in the hand
            tile (tile): What tile this card is on
            unid (str): The unid of this card
            player (int): The unid of the player that owns this card
            changes (dict): Any changes to the card's stats
            renSize (w, h): The size at which to render the card
            intro (bool): Whether or not to play the deck to hand animation
        """
        self.updateDelay = 0
        self.schRender = True
        super().__init__(cardClass, order=order, unid=unid, changes=changes, renSize=renSize, intro=intro)
        self.tile = tile
        
        self.opintro = opintro
        if self.opintro: 
            self.introCycle = -60
            self.blankCard = blankCard(opponent=True)
            
        
        self.arrow = py.image.load("assets/images/arrow.png").convert_alpha()
        self.arrow = py.transform.scale(self.arrow, (100, 100))
        
        if player == None:
            self.player = v.unid
        else:
            self.player = player
            
        self.movePath = None
        self.moveCycle = 0
        
        self.attackTarget = None
        self.attackCycle = 0
        
        self.updateDelay = 0
        self.schRender = False
        self.schRenderSize = None
        
        self.range = 0
        for i in self.card.effects:
            if i.split(" ")[0] == "ranged":
                self.range = int(i.split(" ")[1])
        
        self.update()
        self.attackWon = False
    
    def _render(self, size=None):
        self.schRender = True
        self.schRenderSize = size
        if self.updateDelay <= 0:
            self._base_render(size)
            
            #render attack
            font = py.font.Font("assets/fonts/Galdeano.ttf", int(80/770 * self.size[0]))
            render = font.render(str(self.card.attack + self.changes["attack"]), 1, (0, 0, 0))
            self.image.blit(render, (165/770 * self.size[0] - render.get_rect().size[0]/2, 590/1105 * self.size[1] - render.get_rect().size[1]/2))
            
            #render speed
            render = font.render(str(self.card.speed + self.changes["speed"]), 1, (0, 0, 0))
            self.image.blit(render, (385/770 * self.size[0] - render.get_rect().size[0]/2, 590/1105 * self.size[1] - render.get_rect().size[1]/2))
            
            #render health
            render = font.render(str(self.card.health + self.changes["health"]), 1, (0, 0, 0))
            self.image.blit(render, (610/770 * self.size[0] - render.get_rect().size[0]/2, 590/1105 * self.size[1] - render.get_rect().size[1]/2))
            
            self._render_description()
            self.schRender = False
    
    def _opintro(self):
        pos = (640, 200)
        if self.introCycle > 0:
            end = self.tile.rect.center
            diff = (end[0] - pos[0], end[1] - pos[1])
            diff = (diff[0]/40, diff[1]/40)
            if self.introCycle >= 40:
                self.opintro = False
            pos = (pos[0] + diff[0] * self.introCycle, pos[1] + diff[1] * self.introCycle)
            self.rect.center = pos
            self.rimage = py.transform.scale(self.image, (int(self.rect.size[0] * self.introCycle/40), self.rect.size[1]))
        else:
            self.rimage = py.Surface((0, 0))
            self.blankCard.update()
        self.introCycle += 2
    
    def next_turn(self):
        self.moves = self.card.speed + self.changes["speed"]
        if self.moves == 0:
            self.moves = 1
    
    def move(self, path=None):
        if path != None:
            self.movePath = path
        if self.movePath:
            curIndex = int(self.moveCycle / 50)
            if curIndex > len(self.movePath) - 2:
                self.movePath = []
                self.moveCycle = 0
                self.rect.center = self.tile.rect.center
                return
            curPoint = self.movePath[curIndex]
            endPoint = self.movePath[curIndex + 1]
            #py.Rect(((640 - size*2) + pos[0] * size, (280 - size*1.5) + pos[1] * size), (size, size))
            basex = 415 + curPoint[0] * 150
            basey = 130 + curPoint[1] * 150
            endx = 415 + endPoint[0] * 150
            endy = 130 + endPoint[1] * 150
            diff = ((endx - basex) / 50, (endy - basey) / 50)
            diff = (diff[0] * (self.moveCycle % 50), diff[1] * (self.moveCycle % 50))
            self.rect.center = (basex + diff[0], basey + diff[1])
            self.moveCycle += 6
    
    def attack(self, target=None):
        if target != None:
            self.attackTarget = target
        elif self.attackTarget != None and not self.movePath:
            if type(self.attackTarget) == minionCard:
                if self.attackCycle >= 100:
                    self.attackCycle = 0
                    self.attackTarget._render((100, 140))
                    if self.attackWon:
                        self.movePath = [self.tile.pos, self.attackTarget.tile.pos]
                        self.tile = self.attackTarget.tile
                    self.attackTarget = None
                    self._render((100, 140))
                    return
                self.rect.center = self.tile.rect.center
                for tile in v.tiles:
                    if self.attackTarget.tile == tile:
                        pos = tile.pos
                
                if pos[0] > self.tile.pos[0]:
                    self.rect.x += -0.06 * (self.attackCycle ** 2) + 6 * self.attackCycle
                if pos[0] < self.tile.pos[0]:
                    self.rect.x -= -0.06 * (self.attackCycle ** 2) + 6 * self.attackCycle
                if pos[1] > self.tile.pos[1]:
                    self.rect.y += -0.06 * (self.attackCycle ** 2) + 6 * self.attackCycle
                if pos[1] < self.tile.pos[1]:
                    self.rect.y -= -0.06 * (self.attackCycle ** 2) + 6 * self.attackCycle
            else:
                if self.attackCycle >= 100:
                    self.attackCycle = 0
                    self.attackTarget = None
                    self._render((100, 140))
                    return
                if self.attackTarget == "enemy":
                    self.rect.x += -0.06 * (self.attackCycle ** 2) + 6 * self.attackCycle
                if self.attackTarget == "player":
                    self.rect.x -= -0.06 * (self.attackCycle ** 2) + 6 * self.attackCycle
                if self.tile.pos[1] > 1:
                    self.rect.y -= -0.06 * (self.attackCycle ** 2) + 6 * self.attackCycle
                if self.tile.pos[1] < 1:
                    self.rect.y += -0.06 * (self.attackCycle ** 2) + 6 * self.attackCycle
            self.attackCycle += 6
        
    def update(self):
        self._pre_update()
        if self.updateDelay != 0:
            self.updateDelay -= 1
        if self.card.health + self.changes["health"] <= 0:
            if not self.movePath and self.attackTarget == None:
                if self.updateDelay <= 0:
                    self.kill()
        if self.schRender:
            self._render(self.schRenderSize)
        for event in v.events:
            # If the card is allowed to be interacted with
            if v.gameTurn != None and v.gameTurn["player"] == v.unid and self.alive():
                # Begin dragging
                if self.hovered and event.type == py.MOUSEBUTTONDOWN and event.button == 1 and self.player == v.unid:
                    self.drag = True
                    self.dragPoint = (v.mouse_pos[0] - self.rect.x, v.mouse_pos[1] - self.rect.y)
                    v.dragCard = self
                    v.availableTiles = py.sprite.Group()
                # End Dragging
                if event.type == py.MOUSEBUTTONUP and event.button == 1 and self.drag:
                    self.drag = False
                    v.dragCard = None
                    v.availableTiles = None
                    self.preCard = []
                    self.postCard = []
                    # Card in hand
                    if self.tile == None:
                        if v.pMana >= self.card.cost:
                            for tile in v.tiles:
                                if tile.hovered:
                                    self.tile = tile
                            if self.tile != None:
                                v.pMana -= self.card.cost
                                v.networkEvents.append({"type": "place", "id": self.card.id, "position": self.tile.pos, "unid": self.unid})
                                self._render((100, 140))
                                for card in v.gameCards:
                                    if card.tile == None:
                                        if card.order > self.order:
                                            card.order -= 1
                    # Card on board
                    else:
                        if v.hoverTile == None:
                            pass
                        # If a tile is being hovered
                        else:
                            # If the hovered tile isn't the current tile
                            if v.hoverTile != self.tile:
                                # If the hovered tile is attackable
                                if v.hoverTile.attack:
                                    if self.range == 0:
                                        path = pathfind.pathfind((self.tile.pos[0] + 1, self.tile.pos[1]), (v.hoverTile.pos[0] + 1, v.hoverTile.pos[1]), pathfind.get_grid(skip=[v.hoverTile], castle=True))
                                        path = [(p[0]-1, p[1]) for p in path]
                                        self.movePath = path[:-1]
                                        while self.movePath[-1][0] > 3 or self.movePath[-1][0] < -1:
                                            self.movePath = self.movePath[:-1]
                                        if len(path) < 2:
                                            print("Bad path length", path, self.movePath)
                                        pos = self.movePath[-1]
                                        for tile in v.tiles:
                                            if tile.pos == pos:
                                                self.tile = tile
                                        v.networkEvents.append({"type": "move", "unid": self.unid, "position": pos})
                                    self.moves = 0
                                    # If the target is another minion
                                    if v.hoverTile.castle == None:
                                        target = v.hoverTile.card
                                        v.networkEvents.append({"type": "damage", "unid": self.unid, "target": target.unid})
                                        if self.range == 0:
                                            self.changes["health"] -= target.card.attack + target.changes["attack"]
                                        target.changes["health"] -= self.card.attack + self.changes["attack"]
                                        target.updateDelay += 20
                                        self.updateDelay += 20
                                        self.attackTarget = target
                                        if self.range == 0 and target.changes["health"] + target.card.health <= 0 and self.changes["health"] + self.card.health > 0:
                                            v.networkEvents.append({"type": "move", "unid": self.unid, "position": v.hoverTile.pos})
                                            self.attackWon = True
                                    # If the target is a castle
                                    else:
                                        v.networkEvents.append({"type": "damage", "unid": self.unid, "target": v.opUnid})
                                        v.opHealth -= self.card.attack + self.changes["attack"]
                                        self.attackTarget = "enemy"
                                # If the hovered card isn't attackable 
                                else:
                                    path = pathfind.pathfind(self.tile.pos, v.hoverTile.pos, pathfind.get_grid(skip=[v.hoverTile]))
                                    self.movePath = path
                                    self.tile = v.hoverTile
                                    v.networkEvents.append({"type": "move", "unid": self.unid, "position": self.tile.pos})
                                    self.moves -= len(path) - 1
                    if self.alive():
                        if self.moves <= 0:
                            v.networkEvents.append({"type": "movable", "unid": self.unid, "movable": False})
                        else:
                            v.networkEvents.append({"type": "movable", "unid": self.unid, "movable": True})
        if self.tile == None:
            self._hand_update()
        else:
            self.rect = py.Rect((0, 0), (100, 140))
            self.rimage = self.image.copy()
            if self.movePath: # and not (len(self.movePath) <= 1 and self.attackTarget != None)
                #if not (len(self.movePath) == 1 and self.attackTarget != None):
                self.move()
            else:
                self.rect.center = self.tile.rect.center
            if self.attackTarget != None:
                self.attack()
            if self.moves <= 0:
                self.rimage.fill((150, 150, 150), special_flags=py.BLEND_MULT)
        if self.drag and self.tile != None:
            self.preCard = []
            self.postCard = []
            if v.hoverTile != None and v.hoverTile != self.tile:
                if v.hoverTile.castle == None:
                    path = pathfind.pathfind(self.tile.pos, v.hoverTile.pos, pathfind.get_grid(skip=[v.hoverTile]))
                else:
                    path = pathfind.pathfind((self.tile.pos[0] + 1, self.tile.pos[1]), (v.hoverTile.pos[0] + 1, self.tile.pos[1]), pathfind.get_grid(skip=[v.hoverTile], castle=True))
                    path = [(p[0]-1, p[1]) for p in path]
                for i in range(len(path) - 1):
                    arrowRect = py.Rect(0, 0, 100, 100)
                    if path[i + 1][0] > path[i][0]:
                        arrowRect.centery = 130 + path[i][1] * 150
                        arrowRect.left = 415 + path[i][0] * 150 + 50
                        rarrow = self.arrow.copy()
                    if path[i + 1][0] < path[i][0]:
                        arrowRect.centery = 130 + path[i][1] * 150
                        arrowRect.right = 415 + path[i][0] * 150 - 50
                        rarrow = py.transform.rotate(self.arrow, 180)
                    if path[i + 1][1] > path[i][1]:
                        arrowRect.centerx = 415 + path[i][0] * 150
                        arrowRect.top = 130 + path[i][1] * 150 + 50
                        rarrow = py.transform.rotate(self.arrow, -90)
                    if path[i + 1][1] < path[i][1]:
                        arrowRect.centerx = 415 + path[i][0] * 150
                        arrowRect.bottom = 130 + path[i][1] * 150 - 50
                        rarrow = py.transform.rotate(self.arrow, 90)
                    self.preCard.append((rarrow, arrowRect))
                if v.hoverTile.attack:
                    drect = py.Rect(0, 0, 100, 100)
                    drect.center = v.hoverTile.rect.center
                    self.preCard.append((self.damage, drect))
                    font = py.font.Font("assets/fonts/Galdeano.ttf", 30)
                    dmg = font.render(str(-self.card.attack), 1, (0, 0, 0))
                    drect = dmg.get_rect()
                    drect.center = v.hoverTile.rect.center
                    self.preCard.append((dmg, drect))
                    if v.hoverTile.castle == None and self.range == 0:
                        target = v.hoverTile.card
                        drect = py.Rect(0, 0, 100, 100)
                        drect.center = self.tile.rect.center
                        self.postCard.append((self.damage, drect))
                        font = py.font.Font("assets/fonts/Galdeano.ttf", 30)
                        dmg = font.render(str(-target.card.attack), 1, (0, 0, 0))
                        drect = dmg.get_rect()
                        drect.center = self.tile.rect.center
                        self.postCard.append((dmg, drect))
            if v.hoverTile == self.tile:
                self.rarrow = None
            if v.hoverTile == None:
                self.rarrow = None
        if self.opintro:
            self._opintro()
        self.draw()
class castle(py.sprite.Sprite):
    
    def __init__(self, friendly):
        """A castle image.
        
        Args:
            friendly (bool): Whether this is the player's or the opponent's castle.
        """
        super().__init__()
        self.friendly = friendly
        self.rect = py.Rect(0, 0, 200, 200)
        self.image = py.image.load("assets/images/castle.png").convert_alpha()
        self.image = py.transform.scale(self.image, self.rect.size)
        if self.friendly:
            self.rect.center = (180, 280)
        else:
            self.rect.center = (1100, 280)
            self.image.fill((255, 0, 0), special_flags=py.BLEND_MULT)
    
    def draw(self):
        change(v.screen.blit(self.image, self.rect))
    
    def update(self):
        self.draw()

class blankCard(py.sprite.Sprite):
    def __init__(self, order=0, opponent=False):
        """A blank deck card.
        Args:
            order (int): What position the card is in the deck
        """
        super().__init__()
        self.image = py.image.load("assets/images/cards/card_back.png").convert_alpha()
        self.image = py.transform.scale(self.image, (124, 176))
        self.opponent = opponent
        if self.opponent == False:
            self.rot = random.randint(-45, 45)
            self.rimage = py.transform.rotate(self.image, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = (180, 630)
            self.order = order
            self.aniCycle = 0
        else:
            self.rimage = self.image.copy()
            self.rect = self.image.get_rect()
            self.rect.center = (640, -100)
            self.aniCycle = 1
        
        self.alive = True
    
    def draw(self):
        if self.alive:
            change(v.screen.blit(self.rimage, self.rect))
    
    def update(self):
        if self.aniCycle >= 1:
            if self.opponent == False:
                if self.aniCycle <= 40:
                    self.rimage = py.transform.scale(self.image, (int(125 + 30 * self.aniCycle/40), int(176 + 44 * self.aniCycle/40)))
                    diff = self.rot / 40
                    self.rimage = py.transform.rotate(self.rimage, self.rot - diff * self.aniCycle)
                if self.aniCycle < 60:
                    self.rect.x += 8 * 2
                    self.rect.y -= 5 * 2
                if self.aniCycle >= 40 and self.aniCycle <= 60:
                    self.rimage = py.transform.scale(self.image, (int(155 * (2.98 - 0.0495 * self.aniCycle)), 220))
                if self.aniCycle >= 60:
                    v.hand.append(add_card(v.deck.pop(0), len([c for c in v.gameCards if c.tile == None]), intro=True))
                    self.kill()
            else:
                if self.aniCycle <= 40:
                    self.rimage = py.transform.scale(self.image, (int(125 + 30 * self.aniCycle/40), int(176 + 44 * self.aniCycle/40)))
                if self.aniCycle < 60:
                    self.rect.y += 5 * 2
                if self.aniCycle >= 40 and self.aniCycle <= 60:
                    self.rimage = py.transform.scale(self.image, (int(155 * (2.98 - 0.0495 * self.aniCycle)), 220))
                if self.aniCycle >= 60:
                    self.kill()
                    change(self.rect)
                    self.alive = False
            self.aniCycle += 2
        self.draw()

class Effect(py.sprite.Sprite):
    def __init__(self, type, target=None, pos=None, sheet=None, image=None):
        """Plays an animation.
        
        Args:
            type (str): The type of animation to play
            target (Tile/minionCard): The target of the effect
            pos (x, y): The position of the effect (depends on effect)
            sheet (str): Path to a spritesheet for the effect (depends on effect)
            image (str): Path to a image for the effect (depends on effect)
        """
        super().__init__()
        self.type = type
        self.target = target
        if isinstance(self.target, minionCard):
            self.target = self.target.tile
        if self.type == "meteor":
            if self.target != None:
                for card in v.gameCards:
                    if card.tile == self.target:
                        card.updateDelay += 39
            self.sheet = SpriteSheet(sheet, 8, 1)
            self.rimage = self.sheet.images[0]
            self.rect = self.sheet.images[0].get_rect()
            self.rect.center = (-40, -40)
        if self.type == "explosion":
            self.sheet = SpriteSheet(sheet, 2, 5)
            self.rimage = self.sheet.images[0]
            self.rect = self.sheet.images[0].get_rect()
            if pos != None:
                self.rect.center = pos
            elif self.target != None:
                self.rect.center = self.target.rect.center
        self.cycle = 1
        v.effects.add(self)
    
    def draw(self):
        change(v.screen.blit(self.rimage, self.rect))
    
    def update(self):
        if self.type == "meteor":
            if self.cycle >= 39:
                Effect("explosion", target=self.target, sheet="assets/images/effects/explosion1.png")
                self.kill()
            diff = ((40 + self.target.rect.centerx)/40, (40 + self.target.rect.centery)/40)
            self.rect.centerx = -40 + diff[0] * self.cycle
            self.rect.centery = -40 + diff[1] * self.cycle
            self.rimage = self.sheet.images[int(self.cycle / 2) % 8]
            size = self.rimage.get_rect().size
            self.rimage = py.transform.scale(self.rimage, (int(size[0] * 2 * 20/(self.cycle + 20)), int(size[1] * 2 * 20/(self.cycle + 20))))
            self.cycle += 1.5
        if self.type == "explosion":
            if self.cycle >= 18:
                self.kill()
            self.rimage = self.sheet.images[int(self.cycle / 2)]
            self.cycle += 1
        self.draw()