# 8 Puzzle Solver using A* algorithm
# Use Manhatten distance heuristic
# h(n) = abs(x - p) + abs(y - q), x,y are current location, p,q are final distination

from pprint import pprint
import time
import timeit

correctLocation = [[0, 0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
complete = [1, 2, 3, 4, 5, 6, 7, 8, 0]
closed = []

class node(object):
    tl, tm, tr, ml, mm, mr, bl, bm, br = 0, 0, 0, 0, 0, 0, 0, 0, 0
    board = []
    _id = "123456780" 
    f, h, g = 0, 0, 0
    previousID = "123456780"
    childrenNodes = []
    previousNode = ""
    def __init__(self, _tl, _tm, _tr, _ml, _mm, _mr, _bl, _bm, _br):
        self.tl = _tl
        self.tm = _tm
        self.tr = _tr
        self.ml = _ml
        self.mm = _mm
        self.mr = _mr
        self.bl = _bl
        self.bm = _bm
        self.br = _br
        board = []

#Manhatten Hueristic
def manhatten(_node):
    heuristic = 0
    for i in range(3):
        for j in range(3):
            if(_node.board[i][j] is not 0):
                heuristic += abs(i - correctLocation[_node.board[i][j]-1][0]) + abs(j - correctLocation[_node.board[i][j]-1][1])
    return heuristic

#Check if Board is Correct
def check(_node):
    correct = True
    count = 0
    for i in range(3):
        for j in range(3):
            if(_node.board[i][j] is not complete[count]):
                correct = False
                break
            count+=1
    return correct   
#Find Minimal Cost Node 
def minimal(_opened):
    minimalNode = node(0,0,0,0,0,0,0,0,0)
    minimalNode.f = 1000000
    for i in _opened:
        if(i.f < minimalNode.f):
            minimalNode = i
    return minimalNode    
#Assign Node positions/id/previous id/
def assign(_node, _opened, _prevNode):
    _node.board = [[0,0,0],[0,0,0],[0,0,0]]
    _node.board[0][0] = _node.tl
    _node.board[0][1] = _node.tm
    _node.board[0][2] = _node.tr
    _node.board[1][0] = _node.ml  
    _node.board[1][1] = _node.mm 
    _node.board[1][2] = _node.mr 
    _node.board[2][0] = _node.bl 
    _node.board[2][1] = _node.bm 
    _node.board[2][2] = _node.br
    _node._id = str(_node.tl) + str(_node.tm) + str(_node.tr) + str(_node.ml) + str(_node.mm) + str(_node.mr) + str(_node.bl) + str(_node.bm) + str(_node.br)
    alreadyGenerated = False 
    _node.previousID = _prevNode._id    
    if(_prevNode.previousID == _node._id):
        alreadyGenerated = True
    if(alreadyGenerated == False):
        for i in _opened:
            if(_node._id == i._id):
                alreadyGenerated = True
                break        
        for i in closed:
            if(_node._id == i._id):
                alreadyGenerated = True  
                break        
    if(not alreadyGenerated):
        _node.h = manhatten(_node)
        _prevNode.childrenNodes.append(_node)

#Generate possible moves (create graph)
def generateMoves(_node, _opened):
    emptyX = 0
    emptyY = 0
    for i in range(3):
        for j in range(3):
            if(_node.board[i][j] == 0):
                emptyX = i
                emptyY = j
                break
    #create new nodes
    #if its in top left
    if(emptyX == 0 and emptyY == 0):
        newNode1 = node(_node.board[0][1], 0, _node.board[0][2], _node.board[1][0], _node.board[1][1], _node.board[1][2], _node.board[2][0], _node.board[2][1], _node.board[2][2])
        newNode2 = node(_node.board[1][0], _node.board[0][1], _node.board[0][2], 0, _node.board[1][1], _node.board[1][2], _node.board[2][0], _node.board[2][1], _node.board[2][2])
        assign(newNode1, _opened, _node)   
        assign(newNode2, _opened, _node) 
    #if its in top middle
    if(emptyX == 0 and emptyY == 1):
        newNode1 = node(0, _node.board[0][0], _node.board[0][2], _node.board[1][0], _node.board[1][1], _node.board[1][2], _node.board[2][0], _node.board[2][1], _node.board[2][2])
        newNode2 = node(_node.board[0][0], _node.board[0][2], 0, _node.board[1][0], _node.board[1][1], _node.board[1][2], _node.board[2][0], _node.board[2][1], _node.board[2][2])
        newNode3 = node(_node.board[0][0], _node.board[1][1], _node.board[0][2] , _node.board[1][0], 0, _node.board[1][2], _node.board[2][0], _node.board[2][1], _node.board[2][2])
        assign(newNode1, _opened, _node)
        assign(newNode2, _opened, _node)
        assign(newNode3, _opened, _node)   
    #if its in top right
    if(emptyX == 0 and emptyY == 2):
        newNode1 = node(_node.board[0][0], 0, _node.board[0][1], _node.board[1][0], _node.board[1][1], _node.board[1][2], _node.board[2][0], _node.board[2][1], _node.board[2][2])
        newNode2 = node(_node.board[0][0], _node.board[0][1], _node.board[1][2], _node.board[1][0], _node.board[1][1], 0, _node.board[2][0], _node.board[2][1], _node.board[2][2])
        assign(newNode1, _opened,_node)
        assign(newNode2, _opened,_node)      
    #if its in middle left
    if(emptyX == 1 and emptyY == 0):
        newNode1 = node(0, _node.board[0][1], _node.board[0][2], _node.board[0][0], _node.board[1][1], _node.board[1][2], _node.board[2][0], _node.board[2][1], _node.board[2][2])
        newNode2 = node(_node.board[0][0], _node.board[0][1], _node.board[0][2], _node.board[2][0], _node.board[1][1], _node.board[1][2], 0, _node.board[2][1], _node.board[2][2])
        newNode3 = node(_node.board[0][0], _node.board[0][1], _node.board[0][2], _node.board[1][1], 0, _node.board[1][2], _node.board[2][0], _node.board[2][1], _node.board[2][2])
        assign(newNode1, _opened,_node)
        assign(newNode2, _opened,_node)
        assign(newNode3, _opened,_node)
    #if its in middle middle 
    if(emptyX == 1 and emptyY == 1):
        newNode1 = node(_node.board[0][0], 0, _node.board[0][2], _node.board[1][0], _node.board[0][1], _node.board[1][2], _node.board[2][0], _node.board[2][1], _node.board[2][2])
        newNode2 = node(_node.board[0][0], _node.board[0][1], _node.board[0][2], 0, _node.board[1][0], _node.board[1][2], _node.board[2][0], _node.board[2][1], _node.board[2][2])
        newNode3 = node(_node.board[0][0], _node.board[0][1], _node.board[0][2], _node.board[1][0], _node.board[1][2], 0, _node.board[2][0], _node.board[2][1], _node.board[2][2])
        newNode4 = node(_node.board[0][0], _node.board[0][1], _node.board[0][2], _node.board[1][0], _node.board[2][1], _node.board[1][2], _node.board[2][0], 0, _node.board[2][2])
        assign(newNode1, _opened, _node)
        assign(newNode2, _opened, _node)
        assign(newNode3, _opened, _node)
        assign(newNode4, _opened, _node)

    #if its in middle right
    if(emptyX == 1 and emptyY == 2):
        newNode1 = node(_node.board[0][0], _node.board[0][1], 0, _node.board[1][0], _node.board[1][1], _node.board[0][2], _node.board[2][0], _node.board[2][1], _node.board[2][2])
        newNode2 = node(_node.board[0][0], _node.board[0][1], _node.board[0][2], _node.board[1][0], _node.board[1][1], _node.board[2][2], _node.board[2][0], _node.board[2][1], 0)
        newNode3 = node(_node.board[0][0], _node.board[0][1], _node.board[0][2], _node.board[1][0], 0, _node.board[1][1], _node.board[2][0], _node.board[2][1], _node.board[2][2])
        assign(newNode1, _opened, _node)
        assign(newNode2, _opened, _node)
        assign(newNode3, _opened, _node)
    #if its in bottom left
    if(emptyX == 2 and emptyY == 0):
        newNode1 = node(_node.board[0][0], _node.board[0][1], _node.board[0][2], 0, _node.board[1][1], _node.board[1][2], _node.board[1][0], _node.board[2][1], _node.board[2][2])
        newNode2 = node(_node.board[0][0], _node.board[0][1], _node.board[0][2], _node.board[1][0], _node.board[1][1], _node.board[1][2], _node.board[2][1], 0, _node.board[2][2])
        assign(newNode1, _opened, _node)
        assign(newNode2, _opened, _node)
    #if its in bottom middle
    if(emptyX == 2 and emptyY == 1):
        newNode1 = node(_node.board[0][0], _node.board[0][1], _node.board[0][2], _node.board[1][0], 0, _node.board[1][2], _node.board[2][0], _node.board[1][1], _node.board[2][2])
        newNode2 = node(_node.board[0][0], _node.board[0][1], _node.board[0][2], _node.board[1][0], _node.board[1][1], _node.board[1][2], _node.board[2][0], _node.board[2][2], 0)
        newNode3 = node(_node.board[0][0], _node.board[0][1], _node.board[0][2], _node.board[1][0], _node.board[1][1], _node.board[1][2], 0, _node.board[2][0], _node.board[2][2])
        assign(newNode1, _opened, _node)
        assign(newNode2, _opened, _node)
        assign(newNode3, _opened, _node)
    #if its in bottom right  
    if(emptyX == 2 and emptyY == 2):
        newNode1 = node(_node.board[0][0], _node.board[0][1], _node.board[0][2], _node.board[1][0], _node.board[1][1], _node.board[1][2], _node.board[2][0], 0, _node.board[2][1])   
        newNode2 = node(_node.board[0][0], _node.board[0][1], _node.board[0][2], _node.board[1][0], _node.board[1][1], 0, _node.board[2][0], _node.board[2][1], _node.board[1][2])
        assign(newNode1, _opened, _node)
        assign(newNode2, _opened, _node)

#A* Algorithm
def solver(_node, _opened):
    count = 0
    _opened.append(_node)
    while(len(_opened) > 0):
        currNode = minimal(_opened)
        if(check(currNode)):
            closed.append(currNode)
            _opened.remove(currNode)
            break
        generateMoves(currNode, _opened)
        for i in currNode.childrenNodes:
            #print(i.board)
            if(i not in closed):
                tempG = currNode.g + 1
                newPath = False
                if(i in _opened):
                    if(tempG < i.g):
                        i.g = tempG
                        newPath = True
                else:
                    i.g = tempG
                    newPath = True
                    _opened.append(i)
                if(newPath):
                    i.f = i.g + i.h   
                    i.previousNode = currNode
                    
        _opened.remove(currNode)
        closed.append(currNode)

        if(len(_opened) == 0):
            print("Can't Complete")
            break

#Algorithm to see if board is solvable
def getInvCount(grid):
    inv_count = 0
    for i in range(8):
        for j in range(i + 1, 9):
            if(grid[j] and grid[i] and grid[i] > grid[j]):
                inv_count+=1
    return inv_count

#returns whether or board is solvable or not
def isSolvable(grid):
    invCount = getInvCount(grid)
    return invCount%2 == 0

def main():
    print("Welcome to the Puzzle Solver, please insert the starting places, 1 to 8. List values in order starting from top left, going right across each row. Input 0 for empty space")
    tl, tm, tr, ml, mm, mr, bl, bm, br = [int(a) for a in input().split()]
    #Check If Grid Is Solvable
    gridcheck = [tl, tm, tr, ml, mm, mr, bl, bm, br]
    opened = []
    #Time Code
    start_time = time.time()
    #Check if Grid is Solvable First
    if(isSolvable(gridcheck)):
        print("Can be Solved, proceed")
    else:
        print("Cannot be Solved, Exiting")
        return

    #Creating Starting Node
    start = node(tl, tm, tr, ml, mm, mr, bl, bm, br)
    #Adjust Starting Node Previous
    null = node(0,0,0,0,0,0,0,0,0)
    null._id = "0"
    null.previousID = "0"
    null.g = -1
    #Assign First Node Values
    assign(start, opened, null)
    #Start Solving
    solver(start, opened)
    print("Time it Took: ")
    print("--- %s seconds ---" % (time.time() - start_time))
    #Find Process it Took
    backtrack = []
    currNode = closed.pop()
    backtrack.append(currNode)

    currID = currNode.previousNode._id
    while(currID != "0"):
        for i in closed:
            if(currID == i._id):
                currID = i.previousID
                #print(currID)
                backtrack.append(i)
                #time.sleep(1)
                break
    #
    count = 1
    print("Amount of Moves: " + str(len(backtrack)))
    for i in reversed(backtrack):
        print("Move Number: ", count)
        for j in i.board:
            pprint(j)
        count+=1
        time.sleep(1)


if __name__ == "__main__":
    main()
