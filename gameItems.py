import pygame as py
import variables as v
import random
from renderer import *
import pathfind

class SpriteSheet():
    def __init__(self, file_name, rows, columns):
        """Takes an image and splits it into multiple images.
        
        Args:
            file_name (str/pygame.Surface): The image to split.
            rows (int): The number of rows the sprite sheet has.
            columns (int(: The number of columns the sprite sheet has.
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

class tile(py.sprite.Sprite):
    def __init__(self, pos, style):
        """Creates a single game tile.
        
        Tiles are arranged in a grid, and can have cards placed on them.
        
        Args:
            pos x,y ((int, int)): The tile number in the x and y directions.
            style (str): The style id to use.
        """
        super().__init__()
        sheet = SpriteSheet("assets/images/tiles.png", 6, 5)
        size = 150
        
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

        self.hovered = False
        
        self.pos = pos
        self.rimage = self.image
        self.attack = False
    
    def draw(self):
        change(v.screen.blit(self.rimage, self.rect))
    
    def update(self):
        if self.rect.collidepoint(v.mouse_pos):
            self.hovered = True
        else:
            self.hovered = False
        
        self.attack = False
        
        if v.dragCard != None:
            if v.dragCard.tile == None:
                if self.pos[0] < 2:
                    v.availableTiles.add(self)
            else:
                path = pathfind.pathfind(v.dragCard.tile.pos, self.pos, pathfind.get_grid(skip=[]))
                a = False
                for card in v.gameCards:
                    if card.tile == self:
                        if card.player == v.opUnid:
                            a = True
                            path = pathfind.pathfind(v.dragCard.tile.pos, self.pos, pathfind.get_grid(skip=[self]))
                if path != False and len(path) - 1 <= v.dragCard.card.speed:
                    v.availableTiles.add(self)
                    if a:
                        self.attack = True
                    
                    
                
        if v.availableTiles != None:
            if not self in v.availableTiles:
                self.hovered = False
 
        if self.hovered:
            v.hoverTile = self
            self.rimage = self.image.copy()
            self.rimage.fill((255, 255, 255, 200))
        if self.attack:
            self.rimage = self.image.copy()
            self.rimage.fill((255, 0, 0, 200))
        else:
            self.rimage = self.image
        
        self.draw()
            

class card:
    def __init__(self, name, attack, health, speed, description, type, cost, id):
        """A container for information about a single card.
        
        Args:
            name (str): The card's name.
            attack (int): The card's attack.
            health (int): The card's health.
            speed (int): The card's speed.
            description (str): A description of the card's function.
            type (str): What type of card this is.
            cost (int): The mana cost of the card.
            id (str): The unique identifier for the card
        """
        self.name = name
        self.attack = attack
        self.health = health
        self.speed = speed
        self.description = description
        self.type = type
        self.cost = cost
        self.id = id
        
class gameCard(py.sprite.Sprite):
    def __init__(self, cardClass, order=0, tile=None, unid=None, player=None, changes={}, renSize=(770, 1105)):
        """A card that can be placed in the game.
        
        Args:
            cardClass (card): The card class that this object will represent.
            order (int): The position of this card in the player's hand.
        """
        super().__init__()
        self.card = cardClass
        self.order = order
        
        self.changes = {"attack": 0,
                        "health": 0,
                        "speed": 0,
                        "cost": 0}
        self.changes.update(changes)
        
        self._render(renSize)

        self.hovered = False
        self.drag = False
        self.cycle = 0
        self.dragPoint = (0, 0)
        self.tile = tile
        
        self.rect = py.Rect((0, 0), (155, 220))
        self.rect.center = (415 + self.order * (self.rect.width + 10), 630)
                
        self.arrow = py.image.load("assets/images/arrow.png").convert_alpha()
        self.arrow = py.transform.scale(self.arrow, (100, 100))
        
        self.damage = py.image.load("assets/images/damage.png").convert_alpha()
        self.damage = py.transform.scale(self.damage, (100, 100))
        
        self.preCard = []
        self.postCard = []
        
        if unid == None:
            self.unid = "c" + str(v.unid) + str(v.cardUnid)
            v.cardUnid += 1
        else:
            self.unid = unid
        
        if player == None:
            self.player = v.unid
        else:
            self.player = player
        
        self.update()
    
    def _render(self, size):
        self.size = size
        self.image = py.Surface(self.size)
        icon = py.image.load("assets/images/cards/" + self.card.id + ".png").convert()
        icon = py.transform.smoothscale(icon, (round(600/770 * size[0]), round(390/1105 * size[1])))
        self.image.blit(icon, (80/770 * size[0], 170/1105 * size[1]))
        self.blank = py.image.load("assets/images/cards/blank_minion.png").convert_alpha()
        self.blank = py.transform.smoothscale(self.blank, (self.size[0], self.size[1]))
        self.image.blit(self.blank, (0, 0))
        
        fs = int(130/770 * size[0])
        font = py.font.Font("assets/fonts/Galdeano.ttf", fs)
        render = font.render(str(self.card.cost + self.changes["cost"]), 1, (0, 0, 0))
        self.image.blit(render, (85/770 * size[0] - render.get_rect().size[0]/2, 85/1105 * size[1] - render.get_rect().size[1]/2))
        
        while font.size(self.card.name)[0] > 420/770 * size[0]:
            fs -= 1
            font = py.font.Font("assets/fonts/Galdeano.ttf", fs)
        render = font.render(self.card.name, 1, (0, 0, 0))
        self.image.blit(render, (self.size[0]/2 - render.get_rect().width/2, 90/1105 * size[1] - render.get_rect().height/2))
        
        font = py.font.Font("assets/fonts/Galdeano.ttf", int(80/770 * size[0]))
        render = font.render(str(self.card.attack + self.changes["attack"]), 1, (0, 0, 0))
        self.image.blit(render, (165/770 * size[0] - render.get_rect().size[0]/2, 590/1105 * size[1] - render.get_rect().size[1]/2))
        
        render = font.render(str(self.card.speed + self.changes["speed"]), 1, (0, 0, 0))
        self.image.blit(render, (385/770 * size[0] - render.get_rect().size[0]/2, 590/1105 * size[1] - render.get_rect().size[1]/2))
        
        render = font.render(str(self.card.health + self.changes["health"]), 1, (0, 0, 0))
        self.image.blit(render, (610/770 * size[0] - render.get_rect().size[0]/2, 590/1105 * size[1] - render.get_rect().size[1]/2))
        
        #description
        words = self.card.description.split(" ")
        line = ""
        lineNum = 0
        for word in words:
            fsize = font.size(line + word + " ")
            if fsize[0] < 590/770 * size[0]:
                line = line + word + " "
            else:
                render = font.render(line, 1, (0, 0, 0))
                self.image.blit(render, (100/770 * size[0], 670/1105 * size[1] + lineNum * render.get_rect().height))
                lineNum += 1
                line = word + " "
        render = font.render(line, 1, (0, 0, 0))
        self.image.blit(render, (100/770 * size[0], 670/1105 * size[1] + lineNum * render.get_rect().height))
        
    
    def draw(self):
        if self.preCard != []:
            for item in self.preCard:
                change(v.screen.blit(item[0], item[1]))
        change(v.screen.blit(self.rimage, self.rect))
        if self.postCard != []:
            for item in self.postCard:
                change(v.screen.blit(item[0], item[1]))
        
    
    def update(self):
        change(self.rect)
        if self.rect.collidepoint(v.mouse_pos):
            self.hovered = True
        else:
            self.hovered = False
        
        for event in v.events:
            if v.gameTurn != None and v.gameTurn["player"] == v.unid:
                if self.hovered and event.type == py.MOUSEBUTTONDOWN and event.button == 1 and self.player == v.unid:
                    self.drag = True
                    self.dragPoint = (v.mouse_pos[0] - self.rect.x, v.mouse_pos[1] - self.rect.y)
                    v.dragCard = self
                    v.availableTiles = py.sprite.Group()
                if event.type == py.MOUSEBUTTONUP and event.button == 1 and self.drag:
                    self.drag = False
                    v.dragCard = None
                    v.availableTiles = None
                    self.preCard = []
                    self.postCard = []
                    if self.tile == None:
                        for tile in v.tiles:
                            if tile.hovered:
                                self.tile = tile
                        if self.tile != None:
                            v.networkEvents.append({"type": "place", "id": self.card.id, "position": self.tile.pos, "unid": self.unid})
                            self._render((100, 140))
                            for card in v.gameCards:
                                if card.tile == None:
                                    if card.order > self.order:
                                        card.order -= 1
                            
                    else:
                        if v.hoverTile == None:
                            pass
                        else:
                            if v.hoverTile.attack:
                                path = pathfind.pathfind(self.tile.pos, v.hoverTile.pos, pathfind.get_grid(skip=[v.hoverTile]))
                                pos = path[-2]
                                for tile in v.tiles:
                                    if tile.pos == pos:
                                        self.tile = tile
                                v.networkEvents.append({"type": "move", "unid": self.unid, "position": pos})
                                for card in v.gameCards:
                                    if card.tile == v.hoverTile:
                                        target = card
                                v.networkEvents.append({"type": "damage", "unid": self.unid, "target": target.unid})
                                self.changes["health"] -= target.card.attack + target.changes["attack"]
                                target.changes["health"] -= self.card.attack + self.changes["attack"]
                                self._render((100, 140))
                                target._render((100, 140))
                            
                            else:
                                self.tile = v.hoverTile
                                v.networkEvents.append({"type": "move", "unid": self.unid, "position": self.tile.pos})
            
        if self.tile == None:
            if self.cycle < 30 and self.hovered:
                self.cycle += 4
            if self.cycle > 0 and not self.hovered:
                self.cycle -= 4  
            if self.cycle >= 30:
                self.cycle = 30
            if self.cycle <= 0:
                self.cycle = 0
            
            sMod = 1 + self.cycle/60
            
            self.rect = py.Rect((0, 0), (125 * sMod, 175 * sMod))
            self.rimage = py.transform.scale(self.image, self.rect.size)
            self.rect.center = (415 + self.order * (125 + 10), 710 - self.rect.size[1]/2)
            for card in v.gameCards:
                if card.tile == None and card.cycle > 0:
                    if card.order < self.order:
                        self.rect.x += 62 * (1 + card.cycle/60) - 62
                    if card.order > self.order:
                        self.rect.x -= 62 * (1 + card.cycle/60) - 62
        else:
            self.rect = py.Rect((0, 0), (100, 140))
            #self.rimage = py.transform.scale(self.image, self.rect.size)
            self.rimage = self.image
            self.rect.center = self.tile.rect.center
        
        if self.drag and self.tile == None:
            self.rect.x = v.mouse_pos[0] - self.dragPoint[0]
            self.rect.y = v.mouse_pos[1] - self.dragPoint[1]
        
        if self.drag and self.tile != None:
            self.preCard = []
            self.postCard = []
            if v.hoverTile != None and v.hoverTile != self.tile:
                path = pathfind.pathfind(self.tile.pos, v.hoverTile.pos, pathfind.get_grid(skip=[v.hoverTile]))
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
                    
                    for card in v.gameCards:
                        if card.tile == v.hoverTile:
                            target = card
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
        self.draw()

class castle(py.sprite.Sprite):
    
    def __init__(self, friendly):
        """A castle image.
        
        Args:
            friendly (bool): Whether this is the player's or the opponent's castle.
        """
        super().__init__()
        self.friendly = friendly
        self.rect = py.Rect(0, 0, 300, 300)
        self.image = py.image.load("assets/images/castle.png").convert_alpha()
        self.image = py.transform.scale(self.image, self.rect.size)
        if self.friendly:
            self.rect.center = (180, 280)
        else:
            self.rect.center = (1280 - 180, 280)
            self.image.fill((255, 0, 0), special_flags=py.BLEND_MULT)
        
    
    def draw(self):
        change(v.screen.blit(self.image, self.rect))
    
    def update(self):
        self.draw()