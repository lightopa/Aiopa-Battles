import variables as v

def get_grid():
    """Generates a multidimensional array from the game board.
    
    If a tile is empty, it is marked as false. If there is a card on the tile,
    it is marked as true.
    
    Return:
        grid (list): A grid of booleans representing the game board
    """
    grid = [[False, False, False, False],
            [False, False, False, False],
            [False, False, False, False]]
    for card in v.gameCards:
        if card.tile != None:
            grid[card.tile.pos[1]][card.tile.pos[0]] = True
    return grid

class Node:
    def __init__(self, hit, position):
        self.hit = hit
        self.position = position
        self.parent = None
        self.H = 0 # Estimated distance to end
        self.G = 0 # Distance from start
        self.cost = 1
        
def children(point, grid):
    """Get the points surrounding a point"""
    x,y = point.position
    links = []
    for d in [(x-1, y),(x,y - 1),(x,y + 1),(x+1,y)]:
        if d[1] >= 0 and d[0] >= 0:
            if d[1] < len(grid) and d[0] < len(grid[0]):
                links.append(grid[d[1]][d[0]])
    return [link for link in links if link.hit == False]        

def distance(point, point2):
    return abs(point.position[0] - point2.position[0]) + abs(point.position[1] - point2.position[0])

def pathfind(start, end, grid):
    """Find the shortest path between two points.
    
    Args:
        start x,y (int, int): The start point
        end x,y (int,int): The end point
        grid: A two dimensional array Y by X containing booleans.
                True = wall,
                False = open
    
    Return:
        path (list): A list of points that make up the path between the two points
    """
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            grid[y][x] = Node(grid[y][x], (x,y))
    
    start = grid[start[1]][start[0]]
    end = grid[end[1]][end[0]]
    
    openset = [] # All points being considered 
    closedset = []# The points that have already been considered
    
    current = start # Begin with the start point
    
    openset.append(current)
    
    while openset: # If there are items in openset
        current = min(openset, key=lambda o:o.G + o.H) # Finds node with smallest H + G value in openset
        
        if current == end: # If we've reached the end
            path = []
            while current.parent: # Retrace path
                path.append(current)
                current = current.parent
            path.append(current)
            path = path[::-1]
            path = [p.position for p in path]
            return path # Return path
        
        openset.remove(current)
        closedset.append(current)
        
        for node in children(current, grid): # Iterate through nodes surrounding current node
            if node in closedset:
                continue # Move on
            elif node in openset:
                new_g = current.G + current.cost # Calculate distance from start
                if node.G > new_g: # Check if G current G score beaten
                    node.G = new_g
                    node.parent = current
            else:
                node.G = current.G + current.cost
                node.H = distance(node, end)
                node.parent = current
                openset.append(node)
    return False # No path