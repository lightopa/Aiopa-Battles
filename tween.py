tweens = []

class Tween():
    
    def __init__(self, object, fps=60):
        self.object = object
        self.fps = fps
        
    def to(self, properties, duration, ease=None):
        tweens.append(self)
        self.duration = duration * self.fps
        self.ease = ease
        
        self.properties = {}
        for k, v in properties.items():
            if "__" in k:
                if not k.split("__")[0] in self.object.__dict__:
                    print(self.object.__dict__)
                    raise Exception("TweenPropertyError: " + str(k.split("__")[0]) + " is not a property of " + str(type(self.object)))
                self.properties[k] = (self.object.__dict__[k.split("__")[0]].__getattribute__(k.split("__")[1]), v)
            else:
                if not k in self.object.__dict__:
                    print(self.object.__dict__)
                    raise Exception("TweenPropertyError: " + str(k) + " is not a property of " + str(type(self.object)))
                self.properties[k] = (self.object.__dict__[k], v)
        
        self.cycle = 0
        
    def update(self):
        for k, v in self.properties.items():
            diff = v[1] - v[0]
            inc = diff / self.duration
            tot = inc * self.cycle
            if "__" in k:
                self.object.__dict__[k.split("__")[0]].__setattr__(k.split("__")[1], v[0] + tot)
            else:
                self.object.__dict__[k] = v[0] + tot
            self.cycle += 1
            if self.cycle > self.duration:
                tweens.remove(self)
 
def update():
    for t in tweens:
        t.update()            