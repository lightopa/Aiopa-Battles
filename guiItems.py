import pygame as py
import variables as v
import menuItems
import gameItems
from renderer import *
import time
import math

class blackFade(py.sprite.Sprite):
    def __init__(self, limit=255, rate=6, gradient=False):
        """A class that will fade the screen.
        
        Args:
            limit (int): The maximum opacity of the mask - default=255
            rate (int): The rate at which opacity will change - default=6
            gradient (bool): Whether or not to use a white to black radial gradient - default=False
        """
        super().__init__()
        self.limit = limit
        self.rate = 6
        if gradient == False:
            self.image = py.Surface((1280, 720))
            self.image.fill((0, 0, 0))
        else:
            self.image = py.image.load("assets/images/blackGradient.png").convert()
        self.alpha = 0
    def draw(self):
        self.image.set_alpha(self.alpha)
        v.screen.blit(self.image, (0, 0))
    
    def fadeIn(self):
        if self.alpha < self.limit:
            self.alpha += self.rate
            change(py.Rect(0, 0, 1280, 720))
        if self.alpha > self.limit:
            self.alpha = self.limit
        self.draw()
    def fadeOut(self):
        if self.alpha > 0:
            self.alpha -= self.rate
            change(py.Rect(0, 0, 1280, 720))
        if self.alpha < 0:
            self.alpha = 0
        self.draw()


class debug(py.sprite.Sprite):
    def __init__(self):
        """Displays useful data about the game as it is running"""
        super().__init__()
        self.pos = (0, 0)
        self.font = py.font.Font("assets/fonts/FSB.ttf", int(20))
    def update(self):
        self.label = self.font.render("fps: " + str(round(v.clock.get_fps())), 1, (100, 50, 50))
        change(v.screen.blit(self.label, (self.pos[0], self.pos[1])))
        
        self.label = self.font.render("mouse position: " + str(v.mouse_pos), 1, (100, 50, 50))
        change(v.screen.blit(self.label, (self.pos[0], self.pos[1] + 20)))
        
        self.label = self.font.render("ping: " + str(round((sum(v.ping[-10:])/len(v.ping[-10:]))*1000)) + "ms", 1, (100, 50, 50))
        change(v.screen.blit(self.label, (self.pos[0], self.pos[1] + 40)))
        
        if v.debug:
            self.label = self.font.render("debug mode: True", 1, (100, 50, 50))
            change(v.screen.blit(self.label, (self.pos[0], self.pos[1] + 60)))
        
      
class coinScreen(py.sprite.Sprite):
    def __init__(self):
        """A screen displayed at the start of a game to show if the player is going first or second"""
        super().__init__()
        self.black = blackFade(230, 8, True)
        self.joined = False
        self.coinImages = gameItems.SpriteSheet("assets/images/coin.png", 2, 6).images
        self.coinIndex = 0
        self.coinWait = 0
        self.coinSlow = 0
        self.state = "in"
        self.black2 = blackFade()
        self.black2.alpha = 255
        
    def _joined(self):
        self.joined = True
        font = py.font.Font("assets/fonts/Galdeano.ttf", 80)
        if v.gameStarter == v.unid:
            self.text = font.render("You go first", 1, (255, 255, 255))
            self.miniText = None
            v.totalMana += 1
            v.pMana = v.totalMana
        else:
            self.text = font.render("You go second", 1, (255, 255, 255))
            
            font = py.font.Font("assets/fonts/Galdeano.ttf", 30)
            self.miniText = font.render("You start with an extra card, and the first minion you play gains charge", 1, (255, 255, 255))
            
        self.button = menuItems.Button("Begin", (640, 420), 80, (250, 250, 230), (230, 230, 200), "assets/fonts/Galdeano.ttf", "begin", centred=True)
    
    def update(self):
        if self.state == "in":
            self.black.alpha = 230
            self.black.draw()
        elif self.state == "out":
            self.black.fadeOut() 
        
        if self.coinIndex > 11:
            self.coinIndex = 0
        if v.gameStarter == v.unid:
            ti = 0
        else:
            ti = 6
        if self.joined and self.coinSlow >= 15 and int(self.coinIndex) == ti:
            self.coinIndex = ti
        else:
            self.coinIndex += 0.5 - (self.coinSlow / 60)
            self.coinWait += 1
        ci = py.transform.scale(self.coinImages[int(self.coinIndex)], (150, 150))
        
        if v.gameStarter != None and self.coinWait >= 60:
            if self.coinSlow < 15:
                self.coinSlow += 1
        if self.coinSlow >= 15 and int(self.coinIndex) == ti and not self.joined:
            self._joined()
        
        if self.state == "in":
            change(v.screen.blit(ci, (640 - ci.get_rect().width/2, 180 - ci.get_rect().height/2)))
        if self.joined and self.state == "in":
            change(v.screen.blit(self.text, (640 - self.text.get_rect().width/2, 300 - self.text.get_rect().height/2)))
            if self.miniText != None:
                change(v.screen.blit(self.miniText, (640 - self.miniText.get_rect().width/2, 350 - self.miniText.get_rect().height/2)))
                
            self.button.update()
            if self.button.pressed():
                self.state = "out"
                v.pause = False
                v.pauseType = None
        self.black2.fadeOut()

class healthBar(py.sprite.Sprite):
    def __init__(self, friendly):
        """A health indicator that sits underneath each player's catsle.
        
        Args:
            friendly (bool): Is the bar for the player?
        """
        super().__init__()
        self.friendly = friendly
        self.rect = py.Rect(0, 0, 200, 50)
        if self.friendly:
            self.rect.center = (180, 410)
        else:
            self.rect.center = (1100, 410)
        self.image = py.image.load("assets/images/healthBar.png").convert_alpha()
        self.font = py.font.Font("assets/fonts/Galdeano.ttf", 35)
        self.oldHealth = float("inf")
        self.update()
    
    def draw(self):
        change(v.screen.blit(self.rimage, self.rect))
        change(v.screen.blit(self.rtext, (self.rect.centerx - self.rtext.get_rect().width/2, self.rect.centery - self.rtext.get_rect().height/2)))
    
    def update(self):
        if (self.friendly and self.oldHealth != v.pHealth) or (not self.friendly and self.oldHealth != v.opHealth):
            self.rimage = self.image.copy()
            self.rimage.fill((200, 150, 150), special_flags=py.BLEND_MULT)
            if self.friendly:
                r = py.Rect(0, 0, 200 * v.pHealth/20, 50)
                self.rimage.fill((255, 0, 0), rect=r, special_flags=py.BLEND_MULT)
                self.rtext = self.font.render(str(v.pHealth), 1, (0, 0, 0))
                self.oldHealth = v.pHealth
            else:
                r = py.Rect(0, 0, 200 * v.opHealth/20, 50)
                self.rimage.fill((255, 0, 0), rect=r, special_flags=py.BLEND_MULT)
                self.rtext = self.font.render(str(v.opHealth), 1, (0, 0, 0))
                self.oldHealth = v.opHealth
        self.draw()

class timer(py.sprite.Sprite):
    def __init__(self):
        """The timer for current turn"""
        super().__init__()
        self.rect = py.Rect(340, 45, 600, 10)
        self.image = py.Surface(self.rect.size)
        self.image.fill((255, 230, 50))
        py.draw.rect(self.image, (150, 130, 100), (0, 0, 600, 10), 3)
        self.image.set_alpha(150)
        
        self.mask = py.Surface((self.rect.width, self.rect.height - 3))
        self.mask.fill((75, 75, 75))
        self.mask.set_alpha(0)
        
        self.oldTurn = None
        self.update()
    
    def draw(self):
        change(v.screen.blit(self.rimage, self.rect))
        change(v.screen.blit(self.mask, (self.rect.x + v.timeLeft/v.turnLength * 600, self.rect.y + 1.5), (0, 0, 600 - v.timeLeft/v.turnLength * 600, 10)))
    
    def update(self):
        while v.gameTurn == None:
            py.time.delay(10)
        v.timeLeft = v.turnLength - (time.time() - v.gameTurn["time"])
        if v.online == False:
            v.timeLeft = v.turnLength
        
        if self.oldTurn != v.gameTurn["player"] and v.gameTurn != None:
            if v.gameTurn["player"] != v.unid:
                self.rimage = self.image.copy()
                self.rimage.fill((255, 0, 0), special_flags=py.BLEND_MULT)
                self.oldTurn = v.gameTurn["player"]
            else:
                self.rimage = self.image
        
        if v.timeLeft/v.turnLength > 0.25:
            self.rimage.set_alpha(200 - v.timeLeft/v.turnLength * 200)
            self.mask.set_alpha(200 - v.timeLeft/v.turnLength * 200)
        if v.timeLeft <= 0:
            v.timeLeft = 0
        self.draw()

class PlayerTurn(py.sprite.Sprite):
    def __init__(self):
        """An indicator for who's turn it is"""
        self.image = py.image.load("assets/images/turn.png").convert_alpha()
        self.image = py.transform.scale(self.image, (400, 150))
        self.rect = self.image.get_rect()
        self.rect.center = (640, 200)
        self.cycle = 0
        self.update()
    
    def draw(self):
        change(v.screen.blit(self.rimage, self.rect))
    
    def update(self):
        if self.cycle > 0:
            self.rimage = self.image.copy()
            alpha = int(-0.2833 * self.cycle ** 2 + 17.00 * self.cycle)
            self.rimage.fill((255, 255, 255, alpha), special_flags=py.BLEND_RGBA_MULT)
            self.cycle += 1
            if self.cycle >= 60:
                self.cycle = 0
        else:
            self.rimage = py.Surface((0, 0))
        self.draw()

class ManaMeter(py.sprite.Sprite):
    def __init__(self):
        """An indicator for how much mana the player has"""
        super().__init__()
        self.image = py.image.load("assets/images/mana.png").convert_alpha()
        self.image = py.transform.scale(self.image, (20, 20))
        self.bimage = self.image.copy()
        self.bimage.fill((100, 100, 100), special_flags=py.BLEND_MULT)
    
    def draw(self):
        for i in range(v.totalMana):
            r = (30 + i * 30, 500)
            if i > v.pMana - 1:
                change(v.screen.blit(self.bimage, r))
            else:
                change(v.screen.blit(self.image, r))
    
    def update(self):
        self.draw()
        
class endScreen(py.sprite.Sprite):
    def __init__(self):
        """A screen displayed at the end of a game to show if the player won or lost"""
        super().__init__()
        self.black = blackFade(230, 8, True)
        
        if v.winner == v.unid:
            text = "Victory!"
        else:
            text = "Defeat!"
        
        self.texts = py.sprite.Group()    
        self.texts.add(menuItems.Text(text, (640, 150), (255, 255, 255), "assets/fonts/BlackChancery.ttf", 180, centred=True))
        
        self.button = menuItems.Button("Main Menu", (640, 480), 80, (250, 250, 230), (230, 230, 200), "assets/fonts/Galdeano.ttf", "begin", centred=True)
        
        if v.online:
            self.sign = " + " if v.comp[1] > 0 else " "
            self.texts.add(menuItems.Text("Competitive Points:", (640, 280), (255, 255, 255), "assets/fonts/BlackChancery.ttf", 40, centred=True))
            self.comp = menuItems.Text(str(v.comp[0]) + self.sign + str(v.comp[1]), (640, 350), (255, 255, 255), "assets/fonts/FSB.ttf", 100, centred=True)
        
        self.cycle = 0
    
    def update(self):
        self.black.fadeIn()

        self.texts.update()
        
        if v.online:
            if int(self.cycle / 60) + 1 <= abs(v.comp[1]):
                self.comp.text = str(int(v.comp[0] + int(self.cycle / 60) * math.copysign(1, v.comp[1]))) + self.sign + str(int(v.comp[1] - int(self.cycle / 60) * math.copysign(1, v.comp[1])))
                self.cycle += 1 + self.cycle / 60
            else:
                self.comp.text = str(int(v.comp[0] + int(self.cycle / 60) * math.copysign(1, v.comp[1])))
                
            self.comp.update()
            
        self.button.update()
        if self.button.pressed():
            pass