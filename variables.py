i = {}
screen = None
display = None
clock = None
windowWidth = 640
windowHeight = 360
mouse_pos = (0, 0)
events = []
fullscreen = False
pause = False
pauseType = None
changes = []
oldChanges = []
networkEvents = []
networkChanges = []
ping = [0]
cardUnid = 0
turnLength = 40
timeLeft = turnLength
debug = False

name = ""
pHealth = 20

cards = {}
deck = []
tiles = None
gameCards = None
gameDeck = None
availableTiles = None
dragCard = None
hoverTile = None
effects = None
pturn = None

server = "http://127.0.0.1:5000/"
unid = 0
opUnid = None
opName = None
opHealth = 20
game = None
networkHalt = False
serverConnected = False
gameStarter = None
gameTurn = None
gameStop = None
