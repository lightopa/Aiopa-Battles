import cProfile
import pstats
import os
import time
import sys
import network

try:
    from raven import Client
except:
    sys.path.append("lib")
    from raven import Client

import states

#import hanging_threads
import atexit
import traceback
import variables as v

@atexit.register
def what_happened():
    print("EXIT")


#states.boot()
def crashHandler():
    name = "logs/crash reports/Crash Report " + time.strftime("%Y-%m-%d_%H.%M.%S") + ".txt"
    with open(name, "w") as crash:
        t = traceback.format_exc()
        t = t.replace("\\", "/")
        t = t.split("\n")[0] + "\n" + "\n".join(t.split("\n")[12:])#[12:]
        crash.write(t)
    with open(name, "r") as crash:
        states.crash(crash.read())


if __name__ == "__main__":
    client = Client('https://cc2ec006b88948d79766c93c41ad1346:4a0c698e2fe4499d9ee728a8a91138f3@sentry.io/114800')
    os.makedirs("logs", exist_ok=True)
    os.makedirs("logs/crash reports", exist_ok=True)
    
    try:
        cProfile.run("states.boot()", "logs/Out.txt")
    except Exception as e:
        traceback.print_exc()
        v.networkHalt = True
        network.gameLeave("crash")
        crashHandler()
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