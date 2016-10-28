import pygame as py
import variables as v
from renderer import *

class Button(py.sprite.Sprite):

    def __init__(self, text, pos, size, normalcolour, hovercolour, font, ID, centred = False, bsize=(0,0)):
        """A simple button.
        
        Args:
            text (str): The button text to display.
            pos x,y ((int, int)): The position of the button.
            size (int): The font size of the text.
            normalcolour r,g,b ((int, int, int)): The colour of the button normally.
            hovercolour r,g,b ((int, int, int)): The colour of the button when hovered.
            font (str): The text font file to load.
            ID (str/int): A unique id to identify the button.
            centred (bool): Whether or not the button is centred - default=False
            bsize w,h ((int, int)): The width and height of the button - default=text
        """
        super().__init__()
        self.ID = ID
        self.hovered = False
        self.text = text
        self.pos = pos
        self.hcolour = hovercolour
        self.ncolour = normalcolour
        self.font = font
        if font == None:
            font = "Resources/Fonts/FSB.ttf"
        self.font = py.font.Font(font, int(size))
        self.centred = centred
        self.size = bsize
        self.rend = self.font.render(self.text, True, (0,0,0))
        self.set_rect()
    
    def update(self):
        self.hovered = self.rect.collidepoint(v.mouse_pos)
        if self.hovered:
            colour = self.hcolour
        else:
            colour = self.ncolour
        change(py.draw.rect(v.screen, colour, self.rect))
        v.screen.blit(self.rend, self.rect)

    def set_rect(self):
        self.rect = self.rend.get_rect()
        if not self.centred:
            self.rect.topleft = self.pos
        if self.centred:
            self.rect.center = self.pos
        
        if not self.size[0] == 0:
            self.rect.width = self.size[0]
        if not self.size[1] == 0:
            self.rect.height = self.size[1]

    def pressed(self):
        for event in v.events:
            if self.hovered:
                if event.type == py.MOUSEBUTTONDOWN:
                    return True
            if event.type == py.KEYDOWN:
                if event.key == py.K_RETURN:
                    if self.ID == "continue":
                        return True
        return False
    
class Text(py.sprite.Sprite):
    
    def __init__(self, text, pos, colour, font, size, centred = False):
        """A simple text label.
        
        Args:
            text (str): The text to display.
            pos x,y ((int, int)): The position of the text.
            colour r,g,b ((int, int, int)): The colour of the text.
            font (str): The text font file to load.
            size (int): The font size of the text.
            centred (bool): Whether or not the text is centred - default=False
        """
        super().__init__()
        self.text = text
        self.pos = pos
        self.colour = colour
        self.font = font
        self.size = size
        self.centred = centred
        
    def update(self):
        pos = self.pos
        font = py.font.Font(self.font, self.size)
        label = font.render(self.text, 1, self.colour)
        if self.centred:
            pos = list(self.pos)
            pos[0] -= font.size(self.text)[0] / 2
            pos[1] -= font.size(self.text)[1] / 2
            pos = tuple(pos)
        change(v.screen.blit(label, pos))