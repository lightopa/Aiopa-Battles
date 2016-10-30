import variables as v
import pygame as py

def change(rect):
    """Adds a rect to the changes list.
    
    Args:
        rect (pygame.Rect): The rect to add to the changes list
    """
    if type(rect) != py.Rect:
        raise TypeError(str(rect) + " is not a Rect object")
    v.changes.append(rect)
    
def refresh():
    """Updates the display"""
    for event in v.events:
        if event.type == py.KEYDOWN:
            if event.key == py.K_F11:
                v.fullscreen = not v.fullscreen
                if v.fullscreen:
                    v.display = py.display.set_mode((1280, 720), py.FULLSCREEN)
                    v.windowHeight = 720
                    v.windowWidth = 1280
                else:
                    v.display = py.display.set_mode((640, 360))
                    v.windowHeight = 360
                    v.windowWidth = 640
                change(py.Rect(0, 0, 1280, 720))
    
    if (v.windowWidth, v.windowHeight) == (1280, 720):
        v.display.blit(v.screen, (0, 0))
    else:
        screen_rect = py.Rect(0, 0, v.windowWidth, v.windowHeight)
        image_rect = py.Rect(0, 0, 1280, 720)
        fit_to_rect = image_rect.fit(screen_rect)
        fit_to_rect.center = screen_rect.center
        if True: #smooth scale
            py.transform.smoothscale(v.screen, fit_to_rect.size, v.display)
        else:
            py.transform.scale(v.screen, fit_to_rect.size, v.display)
        
        for c in v.changes:
            c.x /= 2
            c.y /= 2
            c.width /= 2
            c.height /= 2
    
    changes = v.changes + v.oldChanges
    v.oldChanges = v.changes
    if (v.windowWidth, v.windowHeight) != (1280, 720):
        scale = ((1280, 720)[0]/fit_to_rect[2], (1280, 720)[1]/fit_to_rect[3])
        x,y = py.mouse.get_pos()
        v.mouse_pos = (int((x - fit_to_rect[0])*scale[0]), int((y - fit_to_rect[1])*scale[1]))
    else:
        v.mouse_pos = py.mouse.get_pos()
    
    if py.key.get_pressed()[py.K_r]: # highlight updated areas
        for c in changes:
            py.draw.rect(v.display, (255, 0, 0), c, 3)
    
    py.display.update(changes)
    v.changes = []