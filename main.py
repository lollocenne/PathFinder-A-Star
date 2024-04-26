import pygame
from node import *


WIDTH: int = 820
HEIGHT: int = 570

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PathFinder A*")

grid: list[list[Node]] = []
ROWS: int = 15
COLS: int = 10

#nodes:
#   contains a list of all the active node
#   contains the target node
nodes: dict[str:list[Node], str:Node] = {"active": [], "target": None}

path: list[Node] = []

def creteGrid() -> None:
    for x in range(ROWS):
        col = []
        for y in range(COLS):
            col.append(Node(x, y))
        grid.append(col)
    
    for row in grid:
        for col in row:
            col.setNeighbors(grid)
    
    startx = 0
    starty = 2
    
    grid[startx][starty].state = "active"
    grid[ROWS-1][COLS-1].state = "target"
    
    grid[startx][starty].path = [grid[startx][starty]]
    
    for y in range(2, 10):
        grid[7][y].state = "wall"
    
    nodes["active"].append(grid[startx][starty])
    nodes["target"] = grid[ROWS-1][COLS-1]

creteGrid()

def drawGrid() -> None:
    NODE_SIZE: int = 50
    n = 5
    
    for row in grid:
        for node in row:
            if node.state == None:
                pygame.draw.rect(WINDOW, (200, 200, 200), pygame.Rect(node.x * (NODE_SIZE + n), node.y * (NODE_SIZE + n), NODE_SIZE, NODE_SIZE))
            elif node.state == "active":
                pygame.draw.rect(WINDOW, (255, 255, 0), pygame.Rect(node.x * (NODE_SIZE + n), node.y * (NODE_SIZE + n), NODE_SIZE, NODE_SIZE))
            elif node.state == "target":
                pygame.draw.rect(WINDOW, (255, 0, 0), pygame.Rect(node.x * (NODE_SIZE + n), node.y * (NODE_SIZE + n), NODE_SIZE, NODE_SIZE))
            elif node.state == "used":
                pygame.draw.rect(WINDOW, (200, 0, 200), pygame.Rect(node.x * (NODE_SIZE + n), node.y * (NODE_SIZE + n), NODE_SIZE, NODE_SIZE))
            elif node.state == "wall":
                pygame.draw.rect(WINDOW, (0, 0, 255), pygame.Rect(node.x * (NODE_SIZE + n), node.y * (NODE_SIZE + n), NODE_SIZE, NODE_SIZE))
            elif node.state == "path":
                pygame.draw.rect(WINDOW, (0, 100, 0), pygame.Rect(node.x * (NODE_SIZE + n), node.y * (NODE_SIZE + n), NODE_SIZE, NODE_SIZE))

def update():
    completed = isCompleted()
    
    if completed:
        for n in path:
            n.state = "path"
    else:
        nodes["active"].append(activateNode(nodes["active"], nodes["target"]))
print("a")
def isCompleted() -> bool:
    DIRECTIONS = {(0, 1), (1, 0), (0, -1), (-1, 0)}
    for d in DIRECTIONS:
            x = nodes["target"].x + d[0]
            y = nodes["target"].y + d[1]
            
            #check if the node exist in the grid
            if x >= 0 and y >= 0 and x < ROWS and y < COLS:
                if grid[x][y].state == "active" or grid[x][y].state == "path":
                    grid[x][y].state = "path"
                    path.extend(grid[x][y].path)
                    
                    return True

#this is the A* algorithm
def activateNode(activeNodes: list[Node], targetNode: Node) -> Node:
    updateActiveNodes()
    
    possibleNode: Node = None
    possibleFValue: int = None
    startNode: Node = None
    
    for n in activeNodes:
        n.updateNeighbors()
        
        for neighbor in n.neighbors:            
            if possibleNode == None:
                possibleNode = neighbor
                possibleFValue = neighbor.f(n, targetNode)
                startNode = n
            else:
                if neighbor.f(n, targetNode) < possibleFValue:
                    possibleNode = neighbor
                    possibleFValue = neighbor.f(n, targetNode)
                    startNode = n
        
    possibleNode.state = "active"
    possibleNode.path = startNode.path.copy()
    possibleNode.path.append(startNode)
    
    return possibleNode

#remove the non active node
def updateActiveNodes() -> None:
    for n in nodes["active"]:
        if n.state != "active":
            nodes["active"].remove(n)

def draw():
    drawGrid()
    
    pygame.display.update()

def main():
    run = True
    
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(20)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
                
        update()
        draw()
    
    pygame.quit()

if __name__ == "__main__":
    main()
