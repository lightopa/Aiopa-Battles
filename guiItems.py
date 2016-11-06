import pygame as py
import variables as v
import menuItems
import gameItems
from renderer import *

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
        """An FPS counter at the top of the screen"""
        super().__init__()
        self.pos = (0, 0)
        self.font = py.font.Font(None, int(20))
    def update(self):
        self.label = self.font.render("fps: " + str(round(v.clock.get_fps())), 1, (100, 50, 50))
        change(v.screen.blit(self.label, (self.pos[0], self.pos[1])))
        
        self.label = self.font.render("mouse position: " + str(v.mouse_pos), 1, (100, 50, 50))
        change(v.screen.blit(self.label, (self.pos[0], self.pos[1] + 20)))
        
        self.label = self.font.render("ping: " + str(round((sum(v.ping[-10:])/len(v.ping[-10:]))*1000)) + "ms", 1, (100, 50, 50))
        change(v.screen.blit(self.label, (self.pos[0], self.pos[1] + 40)))
        
      
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
        
    def _joined(self):
        self.joined = True
        font = py.font.Font("assets/fonts/Galdeano.ttf", 80)
        if v.gameStarter == v.unid:
            self.text = font.render("You go first", 1, (255, 255, 255))
            self.miniText = None
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

class healthBar(py.sprite.Sprite):
    def __init__(self, friendly):
        super().__init__()
        self.friendly = friendly
        self.rect = py.Rect(0, 0, 200, 50)
        if self.friendly:
            self.rect.center = (180, 410)
        else:
            self.rect.center = (1100, 410)
        self.image = py.image.load("assets/images/healthBar.png").convert_alpha()
        self.update()
    
    def draw(self):
        change(v.screen.blit(self.rimage, self.rect))
    
    def update(self):
        self.rimage = self.image.copy()
        self.rimage.fill((200, 150, 150), special_flags=py.BLEND_MULT)
        if self.friendly:
            r = py.Rect(0, 0, 200 * v.pHealth/20, 50)
            self.rimage.fill((255, 0, 0), rect=r, special_flags=py.BLEND_MULT)
        else:
            r = py.Rect(0, 0, 200 * v.opHealth/20, 50)
            self.rimage.fill((255, 0, 0), rect=r, special_flags=py.BLEND_MULT)
        self.draw()