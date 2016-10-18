import pygame as py
import variables as v
import random

class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """
    # This points to our sprite sheet image
    sprite_sheet = None
    images = None

    def __init__(self, file_name, rows, columns):
        """ Constructor. Pass in the file name of the sprite sheet. """

        self.rows = rows
        self.columns = columns

        # Load the sprite sheet.
        if type(file_name) is py.Surface:
            self.sprite_sheet = file_name.convert_alpha()
        else:
            self.sprite_sheet = py.image.load(file_name).convert_alpha()
        self.getGrid()

    def getGrid(self):
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
    
    def update(self):
        v.screen.blit(self.image, self.rect)

class card:
    def __init__(self, name, attack, health, speed, description, type, cost):
        self.name = name
        self.attack = attack
        self.health = health
        self.speed = speed
        self.description = description
        self.type = type
        self.cost = cost
        
class gameCard(py.sprite.Sprite):
    def __init__(self, cardClass, order):
        self.card = cardClass
        self.order = order
        self.size = (770, 1105)
        self.image = py.Surface(self.size)
        icon = py.image.load("assets/images/cards/" + cardClass.name + ".png")
        #icon = py.transform.scale(icon, (97, 63))
        self.image.blit(icon, (80, 170)) #13 28
        self.blank = py.image.load("assets/images/cards/blank_minion.png")
        #self.blank = py.transform.smoothscale(self.blank, (self.size[0], self.size[1]))
        self.image.blit(self.blank, (0, 0))
        
        font = py.font.Font("assets/fonts/Galdeano.ttf", 130)
        render = font.render(self.card.name, 1, (0, 0, 0))
        self.image.blit(render, (self.size[0]/2 - render.get_rect().width/2, 90 - render.get_rect().height/2))
        
        font = py.font.Font("assets/fonts/Galdeano.ttf", 80)
        render = font.render(str(self.card.attack), 1, (0, 0, 0))
        self.image.blit(render, (165 - render.get_rect().size[0]/2, 590 - render.get_rect().size[1]/2))
        
        render = font.render(str(self.card.speed), 1, (0, 0, 0))
        self.image.blit(render, (385 - render.get_rect().size[0]/2, 590 - render.get_rect().size[1]/2))
        
        render = font.render(str(self.card.health), 1, (0, 0, 0))
        self.image.blit(render, (610 - render.get_rect().size[0]/2, 590 - render.get_rect().size[1]/2))
        
        self.hovered = False
        self.cycle = 0
        
        self.rect = py.Rect((0, 0), (155, 220))
        self.rect.center = (415 + self.order * 20, 630)
    
    def update(self):
        if self.rect.collidepoint(v.mouse_pos):
            self.hovered = True
        else:
            self.hovered = False
            sMod = 1
        
        
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
        image = py.transform.scale(self.image, self.rect.size)
        self.rect.center = (415 + self.order * 20, 710 - self.rect.size[1]/2)
            
        """self.rect = py.Rect((0, 0), (155, 220))
        self.rect.center = (415 + self.order * 20, 630)
        if self.rect.collidepoint(v.mouse_pos):
            if self.firstChange:
                self.firstChange = False
                self.image = py.transform.scale(self.image, (self.size[0]*2, self.size[1]*2))
                print(self.rect)
                self.rect = py.Rect(self.rect.x - self.rect.width, 
                                    self.rect.y - self.rect.height,
                                    self.rect.width * 2,
                                    self.rect.height * 2)
                print(self.rect)"""
        v.screen.blit(image, self.rect)
        
class fps(py.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.pos = (640, 20)
        self.font = py.font.Font(None, int(30))
    def update(self):
        self.label = self.font.render(str(int(v.clock.get_fps())), 1, (255, 0, 0))
        v.screen.blit(self.label, self.pos)