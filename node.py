import math

class Node:
    def __init__(self, x: int, y: int):
        self.x, self.y = x, y
        
        self.grid: list[list] = None        
        self.neighbors: list = None
        
        #state:
        #   None: this node is just a node in the grid
        #   active: this node can be used to find the path
        #   target: target node
        #   used: this node has no more neighbors to use
        #   wall: the path can not pass over this node
        #   path: this node is in the path
        self.state: str = None
        
        self.path: list = None
    
    #return the list of all the closest node (up, right, down, left)
    def getCloseNodes(self) -> list:
        closeNodes = []
        
        GRID_ROWS = len(self.grid)
        GRID_COLS = len(self.grid[0])
        
        #               up,   right,    down,    left
        DIRECTIONS = {(0, 1), (1, 0), (0, -1), (-1, 0)}
        
        for d in DIRECTIONS:
            x = self.x + d[0]
            y = self.y + d[1]
            
            #check if the node exist in the grid
            if x >= 0 and y >= 0 and x < GRID_ROWS and y < GRID_COLS:
                closeNodes.append(self.grid[x][y])
        
        return closeNodes
    
    #set the closest note using the class getCloseNodes()
    def setNeighbors(self, grid) -> None:
        self.grid = grid
        
        self.neighbors = self.getCloseNodes()
    
    #remove the neighbors that can not be used (every node that is not None)
    #change self.state to used if it has not neighbors
    def updateNeighbors(self) -> None:
        for n in self.neighbors:
            if n.state != None:
                self.neighbors.remove(n)
        
        if len(self.neighbors) == 0:
            self.state = "used"
    
    #distance from a connected node
    def g(self, node) -> bool:
        return math.sqrt(pow(self.x - node.x, 2) + pow(self.y - node.y, 2))
    
    #distance from the target node
    def h(self, endNode) -> bool:
        return math.sqrt(pow(self.x - endNode.x, 2) + pow(self.y - endNode.y, 2))
    
    #sum of g() and h()
    def f(self, node, endNode) -> bool:
        return self.g(node) + self.h(endNode)
