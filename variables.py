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

cards = {}
tiles = None
gameCards = None
availableTiles = None
dragCard = None
hoverTile = None

server = "http://127.0.0.1:5000/"
unid = 0
game = None
networkHalt = False
serverConnected = False
gameStarter = None
gameTurn = None
