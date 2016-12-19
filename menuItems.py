import pygame as py
import variables as v
from renderer import *
import string
import gameItems
import random

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
            font = "assets/fonts/FSB.ttf"
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
        self.text = str(text)
        self.pos = pos
        self.colour = colour
        self.size = size
        self.centred = centred
        if font == None:
            font = "assets/fonts/FSB.ttf"
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
        self.rect = self.label.get_rect()
        self.rect.topleft = self.rpos
        self.draw()
        
"""class textInput(py.sprite.Sprite):
    
    def __init__(self, pos, fontSize, characters, fontfile, default=[], background=(255, 255, 255), centred=False):
        ""A text input field.
        
        Args:
            pos x,y (int, int): The position of the box
            fontSize (int): The font size
            characters (int): The number of characters
            fontFile (str): The font path
            default (list): The default contents - default=[]
            background r,g,b (int, int, int): Colour of the input box's background - default=white
            centred (bool): Whether to centre the text box - default=False
        ""
        super().__init__()
        self.font = py.font.Font(fontfile, fontSize)
        self.thickness = int(2 * fontSize / 20)
        biggest = "w"
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
        self.draw()"""
        
class TextBox(py.sprite.Sprite):
    #https://github.com/Mekire/pygame-textbox
    def __init__(self, rect, **kwargs):
        """A text input box.
        Args:
            rect (pygame.Rect): The box's rect
        KWargs (optional):
            id: A unique identifier for the sprite
            active (bool): Is the box pre-selected?
            colour (r, g, b): The box's background colour
            font_colour (r, g, b): The font colour
            outline_colour (r, g, b): The colour of the box's outline
            outline_width (int): The width of the box's outline
            active_colour (r, g, b): The outline colour when box is selected
            fontf (str): The path to the font file
            size (int): The size of the font
            centre (bool): Center the box on the point given in rect?
            default (string): The default contents of the box
            max (int): The maximum length of the input
            replace (str): What to replace each character with while drawing (eg. password)
        
        The final contents of the input box is stored in self.final
        """
        super().__init__()
        self.rect = py.Rect(rect)
        self.buffer = []
        self.final = None
        self.rendered = None
        self.render_rect = None
        self.render_area = None
        self.blink = True
        self.blink_timer = 0.0
        self.ACCEPTED = string.ascii_letters+string.digits+string.punctuation+" "
        self.process_kwargs(kwargs)

    def process_kwargs(self,kwargs):
        defaults = {"id": None,
                    "active": True,
                    "colour": py.Color("white"),
                    "font_colour": py.Color("black"),
                    "outline_colour": py.Color("black"),
                    "outline_width": 2,
                    "active_colour": py.Color("blue"),
                    "fontf": "assets/fonts/FSB.ttf",
                    "size": self.rect.height + 4,
                    "centre": True,
                    "default": "",
                    "max": float("inf"),
                    "replace": None}
        for kwarg in kwargs:
            if kwarg in defaults:
                defaults[kwarg] = kwargs[kwarg]
            else:
                raise KeyError("InputBox accepts no keyword {}.".format(kwarg))
        self.__dict__.update(defaults)
        self.font = py.font.Font(self.fontf, self.size)
        if self.centre:
            self.rect.center = self.rect.topleft
        self.buffer = list(self.default)

    def get_event(self):
        for event in v.events:
            if event.type == py.KEYDOWN and self.active:
                if event.key == py.K_BACKSPACE:
                    if self.buffer:
                        self.buffer.pop()
                elif event.unicode in self.ACCEPTED:
                    if len(self.buffer) < self.max:
                        self.buffer.append(event.unicode)
            elif event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                self.active = self.rect.collidepoint(v.mouse_pos)

    def update(self):
        self.get_event()
        new = "".join(self.buffer)
        if new != self.final:
            self.final = new
            if self.replace == None:
                ren = self.final
            else:
                ren = self.replace * len(self.final)
            self.rendered = self.font.render(ren, True, self.font_colour)
            self.render_rect = self.rendered.get_rect(x=self.rect.x + 2,
                                                      centery=self.rect.centery)
            if self.render_rect.width > self.rect.width-6:
                offset = self.render_rect.width-(self.rect.width-6)
                self.render_area = py.Rect(offset,0,self.rect.width-6,
                                           self.render_rect.height)
            else:
                self.render_area = self.rendered.get_rect(topleft=(0,0))
        if py.time.get_ticks() - self.blink_timer > 400:
            self.blink = not self.blink
            self.blink_timer = py.time.get_ticks()
        
        self.draw()

    def draw(self):
        change(self.rect)
        outline_colour = self.active_colour if self.active else self.outline_colour
        outline = self.rect.inflate(self.outline_width * 2, self.outline_width * 2)
        v.screen.fill(outline_colour, outline)
        v.screen.fill(self.colour, self.rect)
        if self.rendered:
            v.screen.blit(self.rendered, self.render_rect, self.render_area)
        if self.blink and self.active:
            curse = self.render_area.copy()
            curse.topleft = self.render_rect.topleft
            v.screen.fill(self.font_colour, (curse.right + 1, curse.y, 2, curse.h))
            
class Animation(py.sprite.Sprite):
    def __init__(self, rect, image, rows, columns, delay):
        super().__init__()
        self.sheet = gameItems.SpriteSheet(image, rows, columns).images
        self.delay = delay
        self.count = 0
        self.rect = py.Rect(rect)
        for i in range(len(self.sheet)):
            #self.sheet[i] = self.sheet[i].convert()
            self.sheet[i] = py.transform.scale(self.sheet[i], self.rect.size)
    
    def draw(self):
        change(self.rect)
        v.screen.blit(self.sheet[self.count], self.rect)
    
    def update(self):
        self.count = int(py.time.get_ticks() / self.delay) % len(self.sheet)
        self.draw()

class ScrollingAnimation(py.sprite.Sprite):
    def __init__(self, image, speed):
        super().__init__()
        self.image = py.image.load(image)
        self.image = py.transform.scale(self.image, self.image.get_rect().fit(py.Rect(0, 0, 1280, 720)).size)
        self.speed = speed
        self.cycle = 0
    
    def draw(self):
        v.screen.blit(self.image, self.rect1)
        v.screen.blit(self.image, self.rect2)
    
    def update(self):
        self.rect1 = self.image.get_rect()
        self.rect1.topleft = (0, 0 + self.cycle)
        
        self.rect2 = self.image.get_rect()
        self.rect2.topleft = (0, -self.rect2.height + self.cycle)
        
        self.cycle += self.speed
        self.draw()

class StarBackground():
    def __init__(self, direction=0, speedmod=1, stars=400):
        self.background = py.image.load("assets/images/menu/starback.png")
        self.stars = py.sprite.Group()
        for i in range(stars):
            self.stars.add(self._Star((random.randint(0, 1280), random.randint(0, 720)), random.randint(12, 32), random.randint(-90, 90), random.uniform(0, 4) * speedmod, random.randint(1, 4), direction))
    
    def update(self):
        v.screen.blit(self.background, (0, 0))
        self.stars.update()
    class _Star(py.sprite.Sprite):
        def __init__(self, pos, size, rotation, speed, num, direction):
            super().__init__()
            self.image = py.image.load("assets/images/menu/star" + str(num) + ".png")
            self.image = py.transform.scale(self.image, (size, size))
            self.image = py.transform.rotate(self.image, rotation)
            self.rect = self.image.get_rect()
            self.rect.center = pos
            self.speed = speed
            self.startx = pos[0]
            self.starty = pos[1]
            self.change = 0
            self.direction = direction
        
        def draw(self):
            change(v.screen.blit(self.image, self.rect))
        
        def update(self):
            change(self.rect)
            self.change += self.speed * (-1 + (2 * (self.direction % 2 == 0))) # If odd * by -1
            if not self.direction % 2:
                self.rect.y = self.starty + self.change
                if self.rect.y > 720 + self.rect.height and self.direction == 0:
                    self.starty = 0 - self.rect.height
                    self.change = 0
                elif self.rect.y < 0 - self.rect.height:
                    self.starty = 720 + self.rect.height
                    self.change = 0
            else:
                self.rect.x = self.startx + self.change
                if self.rect.x > 1280 + self.rect.width and self.direction == 3:
                    self.startx = 0 - self.rect.width
                    self.change = 0
                elif self.rect.x < 0 - self.rect.width:
                    self.startx = 1280 + self.rect.width
                    self.change = 0
            self.draw()
            
class LoadingCircle(py.sprite.Sprite):
    def __init__(self, size, pos=(640, 360)):
        self.inner = py.image.load("assets/images/loading/inner.png")
        self.inner = py.transform.scale(self.inner, (size, size))
        self.outer = py.image.load("assets/images/loading/outer.png")
        self.outer = py.transform.scale(self.outer, (size, size))
        self.rect = self.outer.get_rect()
        self.rect.center = pos
        self.rotation = 0
    
    def draw(self):
        change(v.screen.blit(self.router, self.rect))
        v.screen.blit(self.rinner, self.rect)
    
    def update(self):
        self.rotation += 0.5
        self.rinner = rot_center(self.inner, self.rotation)
        self.router = rot_center(self.outer, -self.rotation)
        self.draw()
        
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = py.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image