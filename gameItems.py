import pygame as py
import variables as v
import random
from renderer import *

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
    
    def draw(self):
        change(v.screen.blit(self.rimage, self.rect))
    
    def update(self):
        if self.rect.collidepoint(v.mouse_pos):
            self.hovered = True
        else:
            self.hovered = False
        
        if v.dragCard != None:
            if v.dragCard.tile == None:
                if self.pos[0] < 2:
                    v.availableTiles.add(self)
            else:
                if (abs(v.dragCard.tile.pos[0] - self.pos[0]) == 1 and v.dragCard.tile.pos[1] == self.pos[1]) or (abs(v.dragCard.tile.pos[1] - self.pos[1]) == 1 and v.dragCard.tile.pos[0] == self.pos[0]):
                    v.availableTiles.add(self)
                    
                
        if v.availableTiles != None:
            if not self in v.availableTiles:
                self.hovered = False
        
        
                
        if self.hovered:
            v.hoverTile = self
            self.rimage = self.image.copy()
            self.rimage.fill((255, 255, 255, 200))
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
    def __init__(self, cardClass, order=0, tile=None, unid=None, player=None):
        """A card that can be placed in the game.
        
        Args:
            cardClass (card): The card class that this object will represent.
            order (int): The position of this card in the player's hand.
        """
        super().__init__()
        self.card = cardClass
        self.order = order
        self.size = (770, 1105)
        self.image = py.Surface(self.size)
        icon = py.image.load("assets/images/cards/" + cardClass.id + ".png").convert()
        #icon = py.transform.scale(icon, (97, 63))
        self.image.blit(icon, (80, 170)) #13 28
        self.blank = py.image.load("assets/images/cards/blank_minion.png").convert_alpha()
        #self.blank = py.transform.smoothscale(self.blank, (self.size[0], self.size[1]))
        self.image.blit(self.blank, (0, 0))
        
        font = py.font.Font("assets/fonts/Galdeano.ttf", 130)
        render = font.render(self.card.name, 1, (0, 0, 0))
        self.image.blit(render, (self.size[0]/2 - render.get_rect().width/2, 90 - render.get_rect().height/2))
        
        render = font.render(str(self.card.cost), 1, (0, 0, 0))
        self.image.blit(render, (85 - render.get_rect().size[0]/2, 85 - render.get_rect().size[1]/2))
        
        font = py.font.Font("assets/fonts/Galdeano.ttf", 80)
        render = font.render(str(self.card.attack), 1, (0, 0, 0))
        self.image.blit(render, (165 - render.get_rect().size[0]/2, 590 - render.get_rect().size[1]/2))
        
        render = font.render(str(self.card.speed), 1, (0, 0, 0))
        self.image.blit(render, (385 - render.get_rect().size[0]/2, 590 - render.get_rect().size[1]/2))
        
        render = font.render(str(self.card.health), 1, (0, 0, 0))
        self.image.blit(render, (610 - render.get_rect().size[0]/2, 590 - render.get_rect().size[1]/2))
        
        
        
        #description
        words = self.card.description.split(" ")
        line = ""
        lineNum = 0
        for word in words:
            size = font.size(line + word + " ")
            if size[0] < 590:
                line = line + word + " "
            else:
                render = font.render(line, 1, (0, 0, 0))
                self.image.blit(render, (100, 670 + lineNum * render.get_rect().height))
                lineNum += 1
                line = word + " "
        render = font.render(line, 1, (0, 0, 0))
        self.image.blit(render, (100, 670 + lineNum * render.get_rect().height))

        self.hovered = False
        self.drag = False
        self.cycle = 0
        self.dragPoint = (0, 0)
        self.tile = tile
        
        self.rect = py.Rect((0, 0), (155, 220))
        self.rect.center = (415 + self.order * 20, 630)
                
        self.arrow = py.image.load("assets/images/arrow.png").convert_alpha()
        self.arrow = py.transform.scale(self.arrow, (100, 100))
        
        self.rarrow = None
        
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
    
    def draw(self):
        if self.rarrow != None:
            change(v.screen.blit(self.rarrow, self.arrowRect))
        change(v.screen.blit(self.rimage, self.rect))
        
    
    def update(self):
        change(self.rect)
        if self.rect.collidepoint(v.mouse_pos):
            self.hovered = True
        else:
            self.hovered = False
        
        for event in v.events:
            if v.gameTurn["player"] == v.unid:
                if self.hovered and event.type == py.MOUSEBUTTONDOWN and event.button == 1 and self.player == v.unid:
                    self.drag = True
                    self.dragPoint = (v.mouse_pos[0] - self.rect.x, v.mouse_pos[1] - self.rect.y)
                    v.dragCard = self
                    v.availableTiles = py.sprite.Group()
                if event.type == py.MOUSEBUTTONUP and event.button == 1 and self.drag:
                    self.drag = False
                    v.dragCard = None
                    v.availableTiles = None
                    self.rarrow = None
                    if self.tile == None:
                        for tile in v.tiles:
                            if tile.hovered:
                                self.tile = tile
                        if self.tile != None:
                            v.networkEvents.append({"type": "place", "id": self.card.id, "position": self.tile.pos, "unid": self.unid})
                            
                    else:
                        if v.hoverTile == None:
                            pass
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
            self.rect.center = (415 + self.order * 20, 710 - self.rect.size[1]/2)
        else:
            self.rect = py.Rect((0, 0), (100, 140))
            self.rimage = py.transform.scale(self.image, self.rect.size)
            self.rect.center = self.tile.rect.center
        
        if self.drag and self.tile == None:
            self.rect.x = v.mouse_pos[0] - self.dragPoint[0]
            self.rect.y = v.mouse_pos[1] - self.dragPoint[1]
        
        if self.drag and self.tile != None:
            if v.hoverTile != None and v.hoverTile != self.tile and v.hoverTile != None:
                self.arrowRect = py.Rect(0, 0, 100, 100)
                if v.hoverTile.pos[0] > self.tile.pos[0]:
                    self.arrowRect.centery = self.tile.rect.centery
                    self.arrowRect.left = self.tile.rect.centerx + 50
                    self.rarrow = self.arrow.copy()
                if v.hoverTile.pos[0] < self.tile.pos[0]:
                    self.arrowRect.centery = self.tile.rect.centery
                    self.arrowRect.right = self.tile.rect.centerx - 50
                    self.rarrow = py.transform.rotate(self.arrow, 180)
                if v.hoverTile.pos[1] > self.tile.pos[1]:
                    self.arrowRect.centerx = self.tile.rect.centerx
                    self.arrowRect.top = self.tile.rect.centery + 50
                    self.rarrow = py.transform.rotate(self.arrow, -90)
                if v.hoverTile.pos[1] < self.tile.pos[1]:
                    self.arrowRect.centerx = self.tile.rect.centerx
                    self.arrowRect.bottom = self.tile.rect.centery - 50
                    self.rarrow = py.transform.rotate(self.arrow, 90)
                
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