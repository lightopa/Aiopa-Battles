screen = None # The surface that everything blits to
display = None # The display surface
clock = None # The main clock - pygame.Clock
windowWidth = 640 # The width to make the window
windowHeight = 360 # The height to make the window
mouse_pos = (0, 0) # The position of the mouse
events = [] # The events list
fullscreen = False # If the game is fullscreen
pause = False # If the game is paused
pauseType = None # Why the game is paused
changes = [] # All rects that have been updated this tick
oldChanges = [] # All rects that were updated last tick
networkEvents = [] # Changes to push to the server
networkChanges = [] # Changes received from the server
ping = [0] # List of gamelopp response times
cardUnid = 0 # The last used card unid
turnLength = 40 # The length of the turn (seconds)
timeLeft = turnLength # The amount of time left in the current turn
debug = False # Debug mode

name = "" # The player's name
pHealth = 20 # The player's  health

cards = {} # All card container objects
deck = [] # The player's deck - list of gameItems.card
tiles = None # pygame.sprite.Group containing all of the gameItems.tile sprites
gameCards = None # pygame.sprite.Group containing all of the gameItems.gameCard sprites
gameDeck = None # pygame.sprite.Group containing all of the tile gameItems.blankCard sprites
availableTiles = None # A list of gameItems.gameCard objects that will accept the current card
dragCard = None # The gameItems.gameCard that is currently being dragged
hoverTile = None # The gameItems.tile that is currently being hovered
effects = None # A pygame.sprite.Group containing all current gameItems.Effect objects
pturn = None # The guiItems.PlayerTurn object

server = "http://127.0.0.1:5000/" # The server to connect to
unid = 0 # The client's unid, generated by the server
opUnid = None # The opponent's unid, generated by the server 
opName = None # The opponent's name
opHealth = 20 # The opponent's health
game = None # The game's name on the server
networkHalt = False # Switched to True to stop all network threads
serverConnected = False # If the client is connected to the server
gameStarter = None # Which player will start the game - tuple
gameTurn = None # Who's turn it is - tuple
gameStop = None # Why the game has ended - string
