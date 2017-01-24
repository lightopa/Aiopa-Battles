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
        self.update(draw=False)
    
    def draw(self):
        change(py.draw.rect(v.screen, self.colour, self.rect))
        v.screen.blit(self.rend, self.textPos)
    
    def update(self, draw=True):
        self.hovered = self.rect.collidepoint(v.mouse_pos)
        if self.hovered:
            self.colour = self.hcolour
        else:
            self.colour = self.ncolour
        
        if draw: self.draw()

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
    
    
class ImageButton(py.sprite.Sprite):

    def __init__(self, image, pos, size, hovercolour, ID, centred=False):
        """A simple button.
        
        Args:
            image (str): The path to the image.
            pos x,y (int, int): The position of the button.
            size w,h (int, int): The dimensions of the button
            hovercolour r,g,b (int, int, int): A tint to apply when hovered
            ID (str/int): A unique id to identify the button.
            centred (bool): Whether or not the button is centred - default=False
        """
        super().__init__()
        self.ID = ID
        self.hovered = False
        self.hcolour = hovercolour
        self.centred = centred
        self.image = py.image.load(image).convert_alpha()
        self.image = py.transform.scale(self.image, size)
        if self.centred:
            self.rect = self.image.get_rect()
            self.rect.center = pos
        else:
            self.rect = py.rect(pos, size)
        self.update()
    
    def draw(self):
        change(v.screen.blit(self.rimage, self.rect))
    
    def update(self):
        self.hovered = self.rect.collidepoint(v.mouse_pos)
        if self.hovered:
            self.rimage = self.image.copy()
            self.rimage.fill(self.hcolour, special_flags=py.BLEND_MULT)
        else:
            self.rimage = self.image
        self.draw()

    def pressed(self):
        for event in v.events:
            if self.hovered:
                if event.type == py.MOUSEBUTTONDOWN:
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
        #v.screen.fill(outline_colour, outline)
        #v.screen.fill(self.colour, self.rect)
        py.draw.rect(v.screen, outline_colour, outline)
        py.draw.rect(v.screen, self.colour, self.rect)
        if self.rendered:
            v.screen.blit(self.rendered, self.render_rect, self.render_area)
        if self.blink and self.active:
            curse = self.render_area.copy()
            curse.topleft = self.render_rect.topleft
            #v.screen.fill(self.font_colour, (curse.right + 1, curse.y, 2, curse.h))
            py.draw.rect(v.screen, self.font_colour, (curse.right + 1, curse.y, 2, curse.h))
            
class Animation(py.sprite.Sprite):
    def __init__(self, rect, image, rows, columns, delay):
        """An object that plays a spritesheet animation.
        Args:
            rect (pygame.Rect/(x, y, w, h): The position and size of the object
            image (str): The path to the spritesheet
            rows (int): The number of rows on the spritesheet
            columns (int): The number of columns on the spritesheet
            delay (int): The delay between each frame
        """
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
        """Scroll an image in an infinate loop.
        Args:
            image (str): The path to the image to scroll
            speed (int): The scroll speed
        """
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
        """Generate a starry/snowy background effect.
        Args:
            direction (int): The direction of the falling stars (0=down, clockwise)
            speedmod (float): What to multiply the randomly generated speed of each partical by
            stars (int): The number of particals to generate
        """
        self.background = py.image.load("assets/images/menu/starback.png")
        self.stars = py.sprite.Group()
        for i in range(stars):
            self.stars.add(self._Star(self, (random.randint(0, 1280), random.randint(0, 720)), random.randint(12, 32), random.randint(-90, 90), random.uniform(0, 4) * speedmod, random.randint(1, 4), direction))
    
    def update(self):
        v.screen.blit(self.background, (0, 0))
        self.stars.update()
    
    class _Star(py.sprite.Sprite):
        def __init__(self, master, pos, size, rotation, speed, num, direction):
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
            self.master = master
            self.oldrect = self.rect
        
        def draw(self):
            #v.screen.blit(self.master.background, self.oldrect, self.oldrect)
            change(v.screen.blit(self.image, self.rect))
        
        def update(self):
            self.oldrect = self.rect.copy()
            change(self.oldrect)
            self.change += self.speed if (self.direction == 0 or self.direction == 3) else self.speed * -1
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
        """The general loading animation.
        
        Args:
            size (int): The square size of the circle
            pos (x, w): The position of the centre of the circle
        """
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
        
class Option(py.sprite.Sprite):
    
    def __init__(self, pos, text, choices, fontsize, ID, type="radio", selected=None, disabled=False):
        """A super class containing several different types of option changing object.
        
        Args:
            pos x,y: The position of the object.
            text (str): The text label for the option.
            choices (list[of strings]): The selectable options.
            fontsize (int): The size of the font.
            ID (str): A unique identifier for the option object.
            type (str): The type of option object -
                        radio > Multiple radio buttons in a line
                        switch > Two radio buttons side by side
                        dropdown > A toggleable dropdown menu
            selected (str): The currently selected option (in choices)
            disabled (bool): If the option is editable
        """
        
        super().__init__()
        self.pos = pos
        self.fontSize = fontsize
        self.font = py.font.Font("assets/fonts/Galdeano.ttf", self.fontSize)
        self.rend = self.font.render(text, 1, (200, 200, 200))
        self.choices = choices
        self.type = type
        self.selected = selected
        self.ID = ID
        self.disabled = disabled
        
        if self.type == "radio":
            lengths = self.rend.get_rect().width
            font = py.font.Font("assets/fonts/Galdeano.ttf", self.fontSize)
            self.choiceButtons = py.sprite.Group()
            for item in choices:
                self.choiceButtons.add(self._button(self.pos[0] + lengths, item, self))
                lengths += font.size(str(item))[0] + 20
        if self.type == "switch":
            self.font = py.font.Font("assets/fonts/Galdeano.ttf", self.fontSize - 10)
            self.rend1 = self.font.render(self.choices[0], 1, (0, 0, 0))
            self.rend2 = self.font.render(self.choices[1], 1, (0, 0, 0))
            self.srect = py.Rect(self.pos[0] + self.rend.get_rect().width + 10, self.pos[1], self.rend1.get_rect().width + 10 + self.rend1.get_rect().width, self.rend1.get_rect().height + 10)
            self.srect1 = py.Rect(self.pos[0] + self.rend.get_rect().width + 10, self.pos[1], self.rend1.get_rect().width + 3, self.rend1.get_rect().height + 10)
            self.srect2 = py.Rect(self.pos[0] + self.rend.get_rect().width + 10 + self.srect1.width + 2, self.pos[1], self.rend2.get_rect().width + 3, self.rend1.get_rect().height + 10)
        if self.type == "dropdown":
            self.dropped = False
            self.dfont = py.font.Font("assets/fonts/Galdeano.ttf", self.fontSize - 20)
            self.drect = py.Rect(self.pos[0] + self.rend.get_rect().width + 10, self.pos[1] + 12,  self.dfont.size(max(self.choices, key=len))[0], self.dfont.size("W")[1])
            self.choiceDrops = py.sprite.Group()
            heights = self.drect.height
            for item in self.choices:
                self.choiceDrops.add(self._drop(self.drect.x, self.drect.y + heights, self.drect.width, item, self))
                heights += self.drect.height
    
    def update(self):
        change(v.screen.blit(self.rend, self.pos))
        if self.type == "radio":
            self.choiceButtons.update()
        if self.type == "switch":
            py.draw.rect(v.screen, (0, 0, 0), self.srect)
            
            if self.selected == self.choices[0]:
                py.draw.rect(v.screen, (50, 200, 200), self.srect1)
            else:
                py.draw.rect(v.screen, (220, 200, 200), self.srect1)
            if self.srect1.collidepoint(v.mouse_pos):
                py.draw.rect(v.screen, (255, 255, 0), self.srect1, 2)
                if py.mouse.get_pressed()[0]:
                    self.selected = self.choices[0]
            else:
                change(py.draw.rect(v.screen, (0, 0, 0), self.srect1, 2))
            change(v.screen.blit(self.rend1, (self.srect1[0] + 3, self.srect1[1] + 3)))
            
            if self.selected == self.choices[1]:
                py.draw.rect(v.screen, (50, 200, 200), self.srect2)
            else:
                py.draw.rect(v.screen, (220, 200, 200), self.srect2)
            if self.srect2.collidepoint(v.mouse_pos):
                py.draw.rect(v.screen, (255, 255, 0), self.srect2, 2)
                if py.mouse.get_pressed()[0]:
                    self.selected = self.choices[1]
            else:
                change(py.draw.rect(v.screen, (0, 0, 0), self.srect2, 2))
            change(v.screen.blit(self.rend2, (self.srect2[0] + 3, self.srect2[1] + 3)))
        
        if self.type == "dropdown":
            change(self.drect)
            self.choiceDrops.update()
            
            if self.drect.collidepoint(v.mouse_pos) and not self.disabled:
                py.draw.rect(v.screen, (255, 255, 0), self.drect)
                for event in v.events:
                    if event.type == py.MOUSEBUTTONDOWN and py.mouse.get_pressed()[0]:
                        self.dropped = not self.dropped
            else:
                py.draw.rect(v.screen, (50, 200, 200), self.drect)
            
            py.draw.rect(v.screen, (0, 0, 0), self.drect, 2)
            rend = self.dfont.render(self.selected, 1, (0, 0, 0))
            v.screen.blit(rend, (self.drect.centerx - rend.get_rect().width/2, self.drect.centery - rend.get_rect().height/2))
            
            if self.disabled:
                s = py.Surface(self.drect.size, py.SRCALPHA)
                s.fill((50, 50, 50, 200))
                change(v.screen.blit(s, self.drect))
    
    class _drop(py.sprite.Sprite):
        
        def __init__(self, posx, posy, width, text, master):
            super().__init__()
            self.posx = posx
            self.posy = posy
            self.master = master
            self.text = text
            font = py.font.Font("assets/fonts/Galdeano.ttf", self.master.fontSize - 20)
            self.rend = font.render(self.text, 1, (0, 0, 0))
            self.rect = py.Rect(posx, posy, width, self.rend.get_rect().height)
        
        def update(self):
            change(self.rect)
            if self.master.dropped:
                if self.master.selected == self.text:
                    py.draw.rect(v.screen, (50, 200, 200), self.rect)
                else:
                    py.draw.rect(v.screen, (220, 200, 200), self.rect)
                
                if self.rect.collidepoint(v.mouse_pos):
                    py.draw.rect(v.screen, (255, 255, 0), self.rect, 2)
                    if py.mouse.get_pressed()[0]:
                        self.master.selected = self.text
                        self.master.dropped = False
                else:
                    py.draw.rect(v.screen, (0, 0, 0), self.rect, 2)
                v.screen.blit(self.rend, (self.rect.centerx - self.rend.get_rect().width/2, self.rect.centery - self.rend.get_rect().height/2))
                
    
    
    class _button(py.sprite.Sprite):
        
        def __init__(self, posx, text, master):
            super().__init__()
            self.posx = posx
            self.text = text
            self.master = master
            self.posy = self.master.pos[1]
    
        def update(self):
            font = py.font.Font("assets/fonts/Galdeano.ttf", self.master.fontSize)
            rend = font.render(str(self.text), 1, (255, 255, 255))
            rect = rend.get_rect()
            rect.topleft = (self.posx, self.posy)
            rect.height += 2
            rect.width += 2
            
            if rect.collidepoint(v.mouse_pos):
                py.draw.rect(v.screen, (255, 200, 0), rect)
                for event in v.events:
                    if event.type == py.MOUSEBUTTONDOWN:
                        self.master.selected = self
                        self.master.outText = self.text
            else:
                py.draw.rect(v.screen, (255, 178, 102), rect)
            
            if self.master.selected == self:
                py.draw.rect(v.screen, (0, 100, 200), rect, 2)
            else:
                py.draw.rect(v.screen, (153, 76, 0), rect, 2)
            
            rect.x += 2
            rect.y += 2
            change(v.screen.blit(rend, rect))



class InfoBubble(py.sprite.Sprite):
    
    def __init__(self, pos, text, direction, fontsize, colour, limit, target="i"):
        """A hoverable icon that displays text.
        
        Args:
            pos x,y: The position of the icon.
            text (str): The text to display.
            direction (str): Where the text is in relation to the icon (right|down)
            fontsize (int): The size of the font.
            colour r,g,b: The colour of the font.
            limit (int): The max amount of characters per line.
            target (str): The object that should be hovered to display the text -
                            Setting this to 'i' will simply display the info icon
        """
        super().__init__()
        self.target = target
        self.pos = list(pos)
        self.direction = direction
        if target == "i":
            self.image = py.image.load("assets/images/info.png").convert_alpha()
            self.image = py.transform.smoothscale(self.image, (60, 60))
            
            self.rect = py.Rect(self.pos[0] - 30, self.pos[1] - 30, 60, 60)
            if self.direction == "down":
                self.pos[1] += 36
            if self.direction == "up":
                self.pos[1] -= 36
            if self.direction == "left":
                self.pos[0] -= 36
            if self.direction == "right":
                self.pos[0] += 36
        
        self.font = py.font.Font("assets/fonts/Galdeano.ttf", fontsize)
        self.renders = []
        
        
        line = ""
        for word in text.split(" "):
            if len(line + " " + str(word)) <= limit:
                line = line + " " + word
            else:
                self.renders.append(self.font.render(line, 1, colour))
                line = ""
                line = line + " " + word
        if not line == "":
            self.renders.append(self.font.render(line, 1, colour))
    
    def update(self):
        hovered = False
        if self.target == "i":
            change(v.screen.blit(self.image, self.rect))
            if self.rect.collidepoint(v.mouse_pos):
                hovered = True
        else:
            if self.target.hovered:
                hovered = True
        if hovered:
            if self.direction == "down":
                ymod = 0
                for line in self.renders:
                    linerect = line.get_rect()
                    change(v.screen.blit(line, (self.pos[0] - linerect.width/2, self.pos[1] + ymod)))
                    ymod += linerect.height + 5
            if self.direction == "right":
                ymod = 0 - ((self.renders[0].get_rect().height + 5) * len(self.renders)) / 2
                for line in self.renders:
                    linerect = line.get_rect()
                    change(v.screen.blit(line, (self.pos[0], self.pos[1] + ymod)))
                    ymod += linerect.height + 5

class MapFlag(py.sprite.Sprite):
    
    def __init__(self, pos, num):
        super().__init__()
        self.num = num
        if v.levels[self.num]["friendly"] == True:
            self.image = py.image.load("assets/images/map/friendly_flag.png")
        else:
            self.image = py.image.load("assets/images/map/enemy_flag.png")
        self.rect = self.image.get_rect()
        self.rect.midbottom = pos
        
        self.hoverImage = py.image.load("assets/images/map/hover_flag.png")
        self.hoverRect = self.hoverImage.get_rect()
        self.hoverRect.center = self.rect.center
        self.hovered = True
    
    
    def draw(self):
        if self.hovered:
            change(v.screen.blit(self.hoverImage, self.hoverRect))
        change(v.screen.blit(self.image, self.rect))
    
    def update(self):
        if self.rect.collidepoint(v.mouse_pos):
            self.hovered = True
            for event in v.events:
                if event.type == py.MOUSEBUTTONDOWN:
                    v.selectedLevel = self.num
                    v.levelDescription = LevelOverview(self.num)
        else:
            self.hovered = False
        self.draw()

class LevelOverview(py.sprite.Sprite):
    
    def __init__(self, num):
        super().__init__()
        self.name = v.levels[num]["name"]
        self.description = v.levels[num]["description"]
        self.rect = py.Rect(0, 0, 800, 500)
        self.rect.center = (640, 970)
        
        self.buttons = py.sprite.Group()
        self.buttons.add(Button("To Battle", (820, 520), 50, (150, 150, 150), (180, 180, 180), "assets/fonts/Galdeano.ttf", "play"))
        self.buttons.add(Button("Back", (290, 520), 50, (150, 150, 150), (180, 180, 180), "assets/fonts/Galdeano.ttf", "back"))
        self._render()
    
    def _render(self):
        self.image = py.Surface((800, 500), flags=py.SRCALPHA)
        back = py.image.load("assets/images/map/level.png").convert_alpha()
        self.image.blit(back, (0, 0))
        
        font = py.font.Font("assets/fonts/MeriendaOne.ttf", 80)
        rend = font.render(self.name, 1, (200, 200, 200))
        self.image.blit(rend, (400 - rend.get_rect().width/2, 40))
        
        font = py.font.Font("assets/fonts/Merienda.ttf", 40)
        line = ""
        ymod = 0
        for word in self.description.split(" "):
            if font.size(line + " " + str(word))[0] <= 700:
                line = line + " " + word
            else:
                rend = font.render(line, 1, (200, 200, 200))
                self.image.blit(rend, (400 - rend.get_rect().width/2, 150 + ymod))
                ymod += rend.get_rect().height + 5
                line = ""
                line = line + " " + word
        if not line == "":
            rend = font.render(line, 1, (200, 200, 200))
            self.image.blit(rend, (400 - rend.get_rect().width/2, 150 + ymod))
    
    def draw(self):
        change(v.screen.blit(self.image, self.rect))
    
    def update(self):
        if self.rect.centery > 360:
            self.rect.centery -= 20
        for button in self.buttons:
            if button.pressed():
                if button.ID == "play":
                    v.leaveMap = True
                if button.ID == "back":
                    v.levelDescription = None
        self.draw()
        if self.rect.centery <= 360:
            self.buttons.update()
        
def rot_center(image, angle):
    """Rotate an image while keeping its center and size.
    
    Args:
        image (py.Surface): The surface to rotate
        angle (float): The angle to rotate the image
    """
    orig_rect = image.get_rect()
    rot_image = py.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image