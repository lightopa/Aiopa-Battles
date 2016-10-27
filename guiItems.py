import pygame as py
import variables as v
import menuItems

class blackFade(py.sprite.Sprite):
    def __init__(self, limit=255, rate=6, gradient=False):
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
        if self.alpha <= self.limit:
            self.alpha += self.rate
        if self.alpha > self.limit:
            self.alpha = self.limit
        self.draw()
    def fadeOut(self):
        if self.alpha > 0:
            self.alpha -= self.rate
        if self.alpha < 0:
            self.alpha = 0
        self.draw()
        
class coinScreen(py.sprite.Sprite):
    def __init__(self):
        self.black = blackFade(230, 8, True)
        font = py.font.Font("assets/fonts/Galdeano.ttf", 80)
        if v.gameStarter == v.unid:
            self.text = font.render("You go first", 1, (255, 255, 255))
            self.miniText = None
        else:
            self.text = font.render("You go second", 1, (255, 255, 255))
            
            font = py.font.Font("assets/fonts/Galdeano.ttf", 30)
            self.miniText = font.render("You start with an extra card, and the first minion you play gains charge", 1, (255, 255, 255))
            
        self.state = "in"
        
        self.button = menuItems.Button("Begin", (640, 420), 80, (250, 250, 230), (230, 230, 200), "assets/fonts/Galdeano.ttf", "begin", centred=True)
    
    def update(self):
        if self.state == "in":
            self.black.alpha = 230
            self.black.draw()
        elif self.state == "stay":
            self.black.draw()
        elif self.state == "out":
            self.black.fadeOut()
        
        v.screen.blit(self.text, (640 - self.text.get_rect().width/2, 300 - self.text.get_rect().height/2))
        if self.miniText != None:
            v.screen.blit(self.miniText, (640 - self.miniText.get_rect().width/2, 350 - self.miniText.get_rect().height/2))
            
        self.button.update()
        if self.button.pressed():
            v.pause = False
            v.pauseType = None