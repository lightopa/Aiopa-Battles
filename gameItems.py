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
        sheet = SpriteSheet("assets/image/tiles.png", 6, 5)
        size = 150
        if style == "grass":
            self.image = sheet.images[random.choice([0, 5])]
        self.image = py.transform.scale(self.image, (size, size))
        self.rect = py.Rect(((640 - size*2) + pos[0] * size, (280 - size*1.5) + pos[1] * size), (size, size))
        
        self.border = py.Surface((size, size), py.SRCALPHA, 32).convert_alpha()
        py.draw.rect(self.border, (200, 255, 200), (0, 0, size, size), 3)
        self.border.fill((255, 255, 255, 50), special_flags=py.BLEND_RGBA_MULT)
    
    def update(self):
        v.screen.blit(self.image, self.rect)
        v.screen.blit(self.border, self.rect)