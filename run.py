import cProfile
import pstats
import os
import time
import sys

import states

try:
    import pygame
except:
    sys.path.append("lib")

#states.boot()

if __name__ == "__main__":
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    cProfile.run("states.boot()", "logs/Out.txt")
    
    with open("logs/Calltime Dump " + time.strftime("%Y-%m-%d_%H.%M.%S") + ".txt", "w") as fc:
        p = pstats.Stats("logs/Out.txt", stream=fc)
        p.strip_dirs()
        d = p.__dict__["stats"]
        funcstats = {}
        
        for k, v in d.items():
            funcstats[k] = v[2]
        p.sort_stats("time").print_stats()