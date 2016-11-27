import cProfile
import pstats
import os
import time
import sys

try:
    from raven import Client
except:
    sys.path.append("lib")
    from raven import Client


import states

import hanging_threads
import atexit

@atexit.register
def what_happened():
    print("EXIT")


#states.boot()

if __name__ == "__main__":
    client = Client('https://cc2ec006b88948d79766c93c41ad1346:4a0c698e2fe4499d9ee728a8a91138f3@sentry.io/114800')
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    try:
        cProfile.run("states.boot()", "logs/Out.txt")
    except:
        if False:
            client.captureException()
    
    with open("logs/Calltime Dump " + time.strftime("%Y-%m-%d_%H.%M.%S") + ".txt", "w") as fc:
        p = pstats.Stats("logs/Out.txt", stream=fc)
        p.strip_dirs()
        d = p.__dict__["stats"]
        funcstats = {}
        
        for k, v in d.items():
            funcstats[k] = v[2]
        p.sort_stats("time").print_stats()