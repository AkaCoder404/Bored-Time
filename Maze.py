# Maze Solver Using A* Algorithm

from pprint import pprint
from math import sqrt
import random
import time;

backtrackinglist = []
solvable = True

class node(object):
    Nid = 0
    x = 0
    y = 0    
    f = 0
    g = 0
    h = 0
    neighbors = []
    previous = []
    wall = False
    
    def __init__(self, _x, _y, _id):
        self.Nid = _id
        self.x = _x
        self.y = _y
        self.f = self.g = self.h = 0
        self.neighbors = []
        self.previous = []
        # Randomly Generate a "Wall"
        if(random.randint(0,100) < 40):
            self.wall = True
#Generate Possible 
def generateNeighbors(maze, _x, _y):
    if(_x > 0 and _x < len(maze) - 1 and _y > 0 and _y < len(maze[0]) - 1):
        #All 8 Directions
        maze[_x][_y].neighbors.append(maze[_x + 1][_y])
        maze[_x][_y].neighbors.append(maze[_x - 1][_y])
        maze[_x][_y].neighbors.append(maze[_x][_y + 1])
        maze[_x][_y].neighbors.append(maze[_x][_y -1 ])
        maze[_x][_y].neighbors.append(maze[_x + 1][_y + 1])
        maze[_x][_y].neighbors.append(maze[_x - 1][_y - 1])
        maze[_x][_y].neighbors.append(maze[_x + 1][_y - 1])
        maze[_x][_y].neighbors.append(maze[_x - 1][_y + 1])
    if(_x == 0): #top row
        if(_y == 0):  # top left corner
            maze[_x][_y].neighbors.append(maze[_x + 1][_y])
            maze[_x][_y].neighbors.append(maze[_x + 1][_y+1])
            maze[_x][_y].neighbors.append(maze[_x][_y+1])
        elif(_y == len(maze[0]) - 1): #top right corner
            maze[_x][_y].neighbors.append(maze[_x + 1][_y])
            maze[_x][_y].neighbors.append(maze[_x][_y-1])
            maze[_x][_y].neighbors.append(maze[_x + 1][_y - 1])
        else: # remaining top row
            maze[_x][_y].neighbors.append(maze[_x + 1][_y])
            maze[_x][_y].neighbors.append(maze[_x][_y + 1])
            maze[_x][_y].neighbors.append(maze[_x][_y - 1])
            maze[_x][_y].neighbors.append(maze[_x + 1][_y + 1])
            maze[_x][_y].neighbors.append(maze[_x + 1][_y - 1])           
    if(_x == len(maze) - 1):  # bottom row
        if(_y == 0): #bottom left corner
            maze[_x][_y].neighbors.append(maze[_x - 1][_y + 1])
            maze[_x][_y].neighbors.append(maze[_x - 1][_y])
            maze[_x][_y].neighbors.append(maze[_x][_y + 1])
        elif(_y == len(maze[0]) - 1): #bottom right corner
            maze[_x][_y].neighbors.append(maze[_x - 1][_y - 1])
            maze[_x][_y].neighbors.append(maze[_x - 1][_y])
            maze[_x][_y].neighbors.append(maze[_x][_y - 1])
        else: # remaining bottom row
            maze[_x][_y].neighbors.append(maze[_x][_y - 1])
            maze[_x][_y].neighbors.append(maze[_x][_y + 1])
            maze[_x][_y].neighbors.append(maze[_x - 1][_y - 1])
            maze[_x][_y].neighbors.append(maze[_x - 1][_y + 1])
            maze[_x][_y].neighbors.append(maze[_x][_y - 1])     
    if(_y == 0 and _x > 0 and _x < len(maze) - 1):
        maze[_x][_y].neighbors.append(maze[_x-1][_y])
        maze[_x][_y].neighbors.append(maze[_x][_y + 1])
        maze[_x][_y].neighbors.append(maze[_x - 1][_y + 1])
        maze[_x][_y].neighbors.append(maze[_x + 1][_y + 1])
        maze[_x][_y].neighbors.append(maze[_x + 1][_y])   
    if(_y == len(maze[0]) - 1 and _x > 0 and _x < len(maze) - 1): 
        maze[_x][_y].neighbors.append(maze[_x-1][_y])
        maze[_x][_y].neighbors.append(maze[_x - 1][_y - 1])
        maze[_x][_y].neighbors.append(maze[_x ][_y - 1])
        maze[_x][_y].neighbors.append(maze[_x + 1][_y - 1])
        maze[_x][_y].neighbors.append(maze[_x + 1][_y]) 

#Create Maze
def initialize(maze, _sizeX, _sizeY):
    count = 0
    for i in range(_sizeX):
        maze.append([])
        for j in range(_sizeY):
            maze[i].append(node(i, j, count))
            count+=1
    for i in range(_sizeX):
        for j in range(_sizeY):
            generateNeighbors(maze, i, j)
            maze[i][j].previous.append(node(10000, 10000, 10000))
         
#Find minimal cost node to pursue
def minimal(_open, _closed):
    minimalcostNode = node(0, 0, 0)
    minimalcostNode.f = 10000
    # Find lowest costing node, return it
    for i in _open:
        if(i.f <= minimalcostNode.f):
            minimalcostNode = i 
    #print("Next Minimal", minimalcostNode.Nid)
    return minimalcostNode
    
#Hueristic - Ecludian Distance
def heuristic(a, b):
    distance = sqrt((a.x - b.x)**2 + (a.y - b.y)**2) 
    return distance

#Back Track to Print Movement
def backtracking(g, start, maze):
    global backtrackinglist
    backtrackinglist.clear()
    backtrack = g
    while(backtrack.Nid != start.Nid):
        #print(maze[backtrack.x][backtrack.y].Nid, "<-", end="")
        backtrack = maze[backtrack.x][backtrack.y].previous[0]
        backtrackinglist.append(maze[backtrack.x][backtrack.y].Nid)
    #print(maze[start.x][start.y].Nid)
    
#A Star Algorithm
def Astar(maze, _start, _end):
    openSet = []
    closedSet = []
    maze[_start.x][_start.y].wall = False
    maze[_end.x][_end.y].wall = False
    _start = maze[_start.x][_start.y]
    openSet.append(_start)    
    #while stuff still in openSet
    while(len(openSet) > 0):
        currNode = minimal(openSet, closedSet)   
        #print("Curr Node: ", currNode.Nid)  
        if(currNode.Nid == _end.Nid):
            backtracking(currNode, _start, maze)
            print("Finished!!!")
            break   
        openSet.remove(currNode)
        closedSet.append(currNode)
        neighbors = currNode.neighbors
    
        for i in neighbors:
            if(i not in closedSet and i.wall == False):
                tempG = currNode.g + 1
                newPath = False
                if(i in openSet):
                    if(tempG < i.g):
                        i.g = tempG
                        newPath = True
                else:
                    i.g = tempG
                    newPath = True
                    openSet.append(i)
                if(newPath):
                    i.h = heuristic(i, _end)
                    i.f = i.g + i.h
                    i.previous[0] = currNode
        backtracking(currNode, _start, maze)
        if(len(openSet) == 0):
            global solvable
            solvable = False
            print("No Path")
            
def main():
    maze = []
    mapSizeX, mapSizeY = [int(a) for a in input("Map Size X and Y: ").split()]
    startx, starty = [int(a) for a in input("Start Location X and Y: ").split()]
    initialize(maze, mapSizeX, mapSizeX)
    
    start = node(startx, starty, 0)
    end = node(mapSizeX - 1, mapSizeY - 1, mapSizeX * mapSizeY - 1)
  
    space = ""
    if(mapSizeX*mapSizeY >= 10):
        space = "  "

    print("Initiated Board: ")
    for i in range(mapSizeX):
        print("[", end=space)
        for j in range(mapSizeY):
            if(maze[i][j].wall == True):
                print("-", end=space)
                if(j != mapSizeY - 1):
                    print(",", end=space)
            else:
                if(maze[i][j].Nid > 99):
                    print(maze[i][j].Nid, end="")
                elif(maze[i][j].Nid > 9):
                    print(maze[i][j].Nid, end=" ")
                else: 
                    print(maze[i][j].Nid, end=space)
                if(j != mapSizeY - 1):
                    print(",", end=space)
        print("]")

    start_time = time.time()
    Astar(maze, start, end)
    end_time = time.time()

    print("Time it Took: " + str(end_time - start_time))
    global solvable
    if (not solvable):
        return 
    backtrackinglist.insert(0, mapSizeX*mapSizeY-1)
    print("Finished Board")
    print("Backtracking list: ", end="")
    print(backtrackinglist)    

    #Finished Board  
    for i in range(mapSizeX):
        print("[", end="")
        for j in range(mapSizeY):
            if(maze[i][j].wall == True):
                print("-", end="")
                if(j != mapSizeY - 1):
                    print("|", end=space)      
            elif(maze[i][j].Nid in backtrackinglist):
                print("*", end="")
                if(j != mapSizeY - 1):
                    print("|", end=space)     
            else:       
                print(" ", end="")
                if(j != mapSizeY - 1):
                    print("|", end=space)  
        print("]")
        
if __name__ == "__main__":
    main()
