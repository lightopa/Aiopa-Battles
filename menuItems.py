import pygame as py
import variables as v
from renderer import *

class Button(py.sprite.Sprite):

    def __init__(self, text, pos, size, normalcolour, hovercolour, font, ID, centred = False, bsize=(0,0)):
        """A simple button.
        
        Args:
            text (str): The button text to display.
            pos x,y (int, int): The position of the button.
            size (int): The font size of the text.
            normalcolour r,g,b (int, int, int): The colour of the button normally.
            hovercolour r,g,b (int, int, int): The colour of the button when hovered.
            font (str): The text font file to load.
            ID (str/int): A unique id to identify the button.
            centred (bool): Whether or not the button is centred - default=False
            bsize w,h (int, int): The width and height of the button - default=text
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
        self.colour = self.ncolour
        self.update()
    
    def draw(self):
        change(py.draw.rect(v.screen, self.colour, self.rect))
        v.screen.blit(self.rend, self.textPos)
    
    def update(self):
        self.hovered = self.rect.collidepoint(v.mouse_pos)
        if self.hovered:
            self.colour = self.hcolour
        else:
            self.colour = self.ncolour
        self.draw()

    def set_rect(self):
        self.rect = self.rend.get_rect()
        if not self.size[0] == 0:
            self.rect.width = self.size[0]
        if not self.size[1] == 0:
            self.rect.height = self.size[1]
            
        if not self.centred:
            self.rect.topleft = self.pos
            self.textPos = self.pos
        if self.centred:
            self.rect.center = self.pos
            self.textPos = (self.rect.centerx - self.rend.get_rect().width/2, self.rect.centery - self.rend.get_rect().height/2)

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
            pos x,y (int, int): The position of the text.
            colour r,g,b (int, int, int): The colour of the text.
            font (str): The text font file to load.
            size (int): The font size of the text.
            centred (bool): Whether or not the text is centred - default=False
        """
        super().__init__()
        self.text = text
        self.pos = pos
        self.colour = colour
        self.size = size
        self.centred = centred
        self.font = py.font.Font(font, self.size)
        
        self.oldText = None
        self.update()
        
    def draw(self):
        change(v.screen.blit(self.label, self.rpos))
    
    def update(self):
        self.rpos = self.pos
        if self.text != self.oldText:
            self.label = self.font.render(self.text, 1, self.colour)
            self.oldText = self.text
        if self.centred:
            self.rpos = list(self.pos)
            self.rpos[0] -= self.font.size(self.text)[0] / 2
            self.rpos[1] -= self.font.size(self.text)[1] / 2
            self.rpos = tuple(self.rpos)
        self.draw()
        
class textInput(py.sprite.Sprite):
    
    def __init__(self, pos, fontSize, characters, fontfile, default=[], background=(255, 255, 255), centred=False):
        """A text input field.
        
        Args:
            pos x,y (int, int): The position of the box
            fontSize (int): The font size
            characters (int): The number of characters
            fontFile (str): The font path
            default (list): The default contents - default=[]
            background r,g,b (int, int, int): Colour of the input box's background - default=white
            centred (bool): Whether to centre the text box - default=False
        """
        super().__init__()
        self.font = py.font.Font(fontfile, fontSize)
        self.thickness = int(2 * fontSize / 20)
        biggest = "W "
        self.rect = py.Rect(pos, self.font.size(biggest * characters))
        if centred:
            self.rect.center = pos
        self.rect.width += fontSize / 1.5
        self.rect.height += fontSize / 1.5
        self.fontSize = fontSize
        self.string = default
        self.characters = characters
        self.shift = False
        self.done = False
        self.outText = ""
        self.background = background
    
    def draw(self):
        change(py.draw.rect(v.screen, self.background, self.rect))
        change(py.draw.rect(v.screen, (0, 0, 0), self.rect, self.thickness))
        x = self.rect.x + self.fontSize / 3
        y = self.rect.y + self.fontSize / 3
        for letter in self.string:
            char = letter
            ren = self.font.render(char, 1, (0, 0, 0))
            change(v.screen.blit(ren, (x, y)))
            x += self.font.size(char)[0] + self.fontSize / 6
    
    def update(self):
        global textEdit
        textEdit = True
        self.outText = "".join(self.string)
        for event in v.events:
            if event.type == py.KEYDOWN:
                if len(self.string) < self.characters:
                    if py.key.name(event.key) in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ',', '.', "'", '/', '#', ';', '-']:
                        if py.key.get_mods() == py.KMOD_LSHIFT:
                            let = py.key.name(event.key).upper()
                            if py.key.name(event.key) == '1':
                                let = '!'
                            if py.key.name(event.key) == '2':
                                let = '"'
                            if py.key.name(event.key) == '3':
                                let = '£'
                            if py.key.name(event.key) == '4':
                                let = '$'
                            if py.key.name(event.key) == '5':
                                let = '%'
                            if py.key.name(event.key) == '9':
                                let = '('
                            if py.key.name(event.key) == '0':
                                let = ')'
                            if py.key.name(event.key) == '/':
                                let = '?'
                            if py.key.name(event.key) == ';':
                                let = ':'
                        else:
                            let = py.key.name(event.key)
                        self.string.append(let)
                    if event.key == py.K_SPACE:
                        self.string.append(" ")
                if event.key == py.K_BACKSPACE:
                    if len(self.string) > 0:
                        self.string.pop(-1)
        self.draw()