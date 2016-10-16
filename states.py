import pygame as py
import variables as v
import menuItems
import network

def boot():
    py.init()
    v.display = py.display.set_mode((640, 360))
    v.screen = py.Surface((1280, 720))
    v.clock = py.time.Clock()
    preload()

def preload():
    assets = [("", ""),
              ("", "")]
    
    v.i = {}
    """for img in assets:
        v.i[img[0]] = py.image.load(img[1])"""
        
    mainMenu()
    
def refresh():
    screen_rect = py.Rect(0, 0, v.windowWidth, v.windowHeight)
    image_rect = py.Rect(0, 0, 1280, 720)
    
    if (v.windowWidth, v.windowHeight) == (1280, 720):
        v.display.blit(v.screen, (0, 0))
        fit_to_rect = image_rect
    else:
        fit_to_rect = image_rect.fit(screen_rect)
        fit_to_rect.center = screen_rect.center
        if False: #smooth scale
            scaled = py.transform.smoothscale(v.screen, fit_to_rect.size)
        else:
            scaled = py.transform.scale(v.screen, fit_to_rect.size)
        v.display.blit(scaled, fit_to_rect)
    
    if (v.windowWidth, v.windowHeight) != (1280, 720):
        scale = ((1280, 720)[0]/fit_to_rect[2], (1280, 720)[1]/fit_to_rect[3])
        x,y = py.mouse.get_pos()
        v.mouse_pos = (int((x - fit_to_rect[0])*scale[0]), int((y - fit_to_rect[1])*scale[1]))
    else:
        v.mouse_pos = py.mouse.get_pos()
    
    py.display.flip()

def mainMenu():
    buttons = py.sprite.Group()
    buttons.add(menuItems.Button("Play", (640, 360), 120, (0, 100, 200), (0, 50, 255), "assets/font/Galdeano.ttf", "play", centred=True))
    while True:
        py.event.pump()
        v.events = []
        v.events = py.event.get()
        v.clock.tick(60)
        
        v.screen.fill((0, 255, 255))
        
        buttons.update()
        
        for button in buttons:
            if button.ID == "play":
                if button.pressed():
                    queue()
                
        refresh()


def queue():
    network.queue()
    while True:
        py.event.pump()
        v.events = []
        v.events = py.event.get()
        v.clock.tick(60)
        
        v.screen.fill((50, 100, 200))
        refresh()