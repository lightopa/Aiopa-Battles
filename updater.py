import urllib.request
import pickle
import sys
import ast
try:
    import variables as v
except:
    class var():
        def __init__(self):
            self.screen = None
    v = var()

import pygame as py
class textLabel(py.sprite.Sprite):
    def __init__(self, text, pos, colour, font, size, variable = False, centred = False):
        super().__init__()
        self.text = text
        self.pos = pos
        self.colour = colour
        self.font = font
        self.size = size
        self.variable = variable
        self.centred = centred
        
    def update(self):
        pos = self.pos
        font = py.font.Font(self.font, self.size)
        if not self.variable:
            label = font.render(self.text, 1, self.colour)
        if self.variable:
            label = font.render(str(getattr(v, self.text)), 1, self.colour)
        if self.centred:
            pos = list(self.pos)
            pos[0] -= font.size(self.text)[0] / 2
            pos[1] -= font.size(self.text)[1] / 2
            pos = tuple(pos)
        v.screen.blit(label, pos)
class Button(py.sprite.Sprite):
    def __init__(self, text, pos, size, hovercolour, normalcolour, font, ID, centred = False, bsize=(0,0)):
        super().__init__()
        self.ID = ID
        self.hovered = False
        self.text = text
        self.pos = pos
        self.hcolour = hovercolour
        self.ncolour = normalcolour
        self.font = font
        self.font = py.font.Font(font, int(size))
        self.centred = centred
        self.size = bsize
        self.set_rect()
    
    def update(self):
        self.set_rend()
        py.draw.rect(v.screen, self.get_color(), self.rect)
        v.screen.blit(self.rend, self.rect)
        if self.rect.collidepoint(py.mouse.get_pos()):
            self.hovered = True
        else:
            self.hovered = False

    def set_rend(self):
        self.rend = self.font.render(self.text, True, (0,0,0))

    def get_color(self):
        if self.hovered:
            return self.hcolour
        else:
            return self.ncolour

    def set_rect(self):
        self.set_rend()
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
        mouse = py.mouse.get_pos()
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False
import os, shutil

theFont = None
py.init()
v.screen = py.display.set_mode((640, 480))
v.screen.fill((20, 20, 20))
textLabel("Checking For Updates...", (320, 240), (255, 255, 255), theFont, 50, False, True).update()
py.display.flip()

tries = 0

def reporthook(count, blockSize, totalSize):
    if totalSize == -1:
        print("FAILED TOTALSIZE")
        raise Exception()
    #Shows percentage of download
    py.event.pump()
    for event in py.event.get():
        if event.type == py.QUIT:
            sys.exit()
    percent = int(count*blockSize*100/totalSize)
    rect = py.Rect(100, 240, percent*4.4, 30)
    v.screen.fill((20, 20, 20))
    py.draw.rect(v.screen, (255, 0, 0), rect)
    py.draw.rect(v.screen, (0, 0, 0), rect, 2)
    py.draw.rect(v.screen, (0, 0, 0), (100, 240, 440, 30), 2)
    textLabel("Downloading...", (320, 150), (255, 255, 255), theFont, 50, False, True).update()
    textLabel(str(percent) + "%", (320, 255), (255, 255, 255), theFont, 20, False, True).update()
    py.display.flip()

def recursive_overwrite(src, dest, ignore=None):
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                recursive_overwrite(os.path.join(src, f), 
                                    os.path.join(dest, f), 
                                    ignore)
    else:
        shutil.copyfile(src, dest)

def updateCheck():
    global latest
    page = urllib.request.urlopen('https://api.github.com/repos/lightopa/aiopa-battles/git/refs/heads/master')
    #print(page.read().decode("utf-8"))
    #data = json.loads(page.read().decode("utf-8"))
    data = ast.literal_eval(page.read().decode("utf-8"))
    latest = data["object"]["sha"]
    
    #ind = page.find('class="sha btn btn-outline"')
    #latest = page[ind + 38:ind + 45]
    #print(latest)
    
    #CHECK IF LATEST IS PROPER
    
    try:
        f = open("Update/current.version", "rb")
        current = pickle.load(f)
        f.close()
    except:
        print("create new file")
        try:
            os.mkdir("Update")
        except:
            pass
        f = open("Update/current.version", "wb")
        current = 0000
        pickle.dump(current, f)
        f.close()
    print(current, "vs", latest)
    if current != latest:
        from os import remove
        try:
            remove("Update/download.zip")
        except:
            pass
         
        print("downloading latest")
        buttons = py.sprite.Group()
        buttons.add(Button("Update", (220, 240), 60, (100, 100, 100), (255, 255, 255), theFont, "Y", centred=True))
        buttons.add(Button("Ignore", (420, 240), 60, (100, 100, 100), (255, 255, 255), theFont, "N", centred=True))
        buttons.add(Button("Skip Update", (320, 300), 40, (100, 100, 100), (255, 255, 255), theFont, "S", centred=True))
        labels = py.sprite.Group()
        labels.add(textLabel("An Update Is Available:", (320, 150), (255, 255, 255), theFont, 50, False, True))
        labels.add(textLabel(str(str(current) + " ==> " + str(latest)), (320, 180), (255, 255, 255), theFont, 20, False, True))
        
        while True:
            py.event.pump()
            v.screen.fill((20, 20, 20))
            buttons.update()
            labels.update()
            for event in py.event.get():
                if event.type == py.QUIT:
                    sys.exit()
                elif event.type == py.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.pressed():
                            id = button.ID
                            if id == "Y":
                                global tries
                                tries = 0
                                download()
                                return
                            if id == "N":
                                return 
                            if id == "S":
                                f = open("Saves/current.version", "wb")
                                current = latest
                                pickle.dump(current, f)
                                f.close()
                                return
            py.display.flip()

    else:
        v.screen.fill((20, 20, 20))
        t = textLabel("No Update!", (320, 250), (255, 0, 0), theFont, 70, False, True)
        v.current = current
        t.update()
        py.display.update()
        if __name__ == "__main__":
            py.time.wait(2000)
        
def download():
    global tries
    try:
        try:
            os.mkdir("Update")
        except:
            pass
        urllib.request.urlretrieve("https://github.com/lightopa/Aiopa-Battles/archive/master.zip", "Update/download.zip", reporthook)
        f = open("Update/current.version", "wb")
        current = latest
        pickle.dump(current, f)
        f.close()
        unzip()
    except Exception as e:
        tries += 1
        print("Error: " + str(e))
        v.screen.fill((20, 20, 20))
        textLabel("Download Error. Retry " + str(tries) + "/8", (320, 240), (255, 255, 255), theFont, 50, False, True).update()
        textLabel("Error: " + str(e), (320, 240), (255, 255, 255), theFont, 50, False, True).update()
        py.display.flip()
        if tries > 8:
            return
        download()

def unzip():
    v.screen.fill((20, 20, 20))
    textLabel("Extracting Data...", (320, 240), (255, 255, 255), theFont, 50, False, True).update()
    py.display.flip()
    import zipfile
    with zipfile.ZipFile('Update/download.zip', "r") as z:
        z.extractall("Update/")
    
    v.screen.fill((20, 20, 20))
    textLabel("Updating Files...", (320, 240), (255, 255, 255), theFont, 50, False, True).update()
    py.display.flip()
    
    from os import getcwd
    recursive_overwrite("Update/Aiopa-Battles-master", getcwd())


if __name__ == "__main__":
    updateCheck()