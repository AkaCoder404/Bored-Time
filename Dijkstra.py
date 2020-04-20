# Uses Dijkstra's algorithm to produce least costly route from start node to each node
# Example: 
# Nodes/Connections/Source: 5 5 1
# Input Connections and Weight

# 1 2 3
# 1 5 8
# 2 3 1
# 3 4 1
# 4 5 1
# Location  --->   Cost --- Path
# 1 --> 1  ------>  0 ---  1 <-1
# 1 --> 2  ------>  3 ---  2 <-1
# 1 --> 3  ------>  4 ---  3 <-2 <-1
# 1 --> 4  ------>  5 ---  4 <-3 <-2 <-1

from pprint import pprint
def minimal(_visited, _cost):
    leastcost = 100000
    leastcost_index = 0
    count = 0
    for i in _cost:
        if (i <= leastcost and count not in _visited):
            leastcost = i
            leastcost_index = count
        count+=1           
    return leastcost_index

def dijk(_nodes, _connections, _source, _graph, _previous, _cost):
    visited = [] #puts all visited nodes here
    _cost[_source] = 0
    _previous[_source] = 0

    while(len(visited) < _nodes):
        nextNode = minimal(visited, _cost)
        visited.append(nextNode)
        for j in range(_nodes):
            #check if node already visited, check if a connection exist, and check if the cost of getting to that node 
            if((j+1) not in visited and _graph[nextNode][j] and _cost[nextNode] != 100000 and _cost[nextNode] + _graph[nextNode][j] < _cost[j]):
                _cost[j] = _cost[nextNode] + _graph[nextNode][j]
                _previous[j] = nextNode
      

def initialize(nodes, connections, _graph, _previous, _cost):
    for i in range(nodes):
        _previous.append(100000)
        _cost.append(100000)
        _graph.append([])
        for j in range(nodes):
            _graph[i].append([])
    
    print("Input Connections and Weight")
    for i in range(connections):
        x, y, z = [int(a) for a in input().split()]
        _graph[x - 1][y - 1] = _graph[y - 1][x - 1] = z   

def main():
    nodes, connections, source = [int(a) for a in input("Nodes/Connections/Source: ").split()]
    graph = []
    previous = []
    cost = []
    initialize(nodes, connections, graph, previous, cost)
    dijk(nodes, connections, source - 1, graph, previous, cost)
    

    print("Location  --->   Cost --- Path ")
    for i in range(nodes - 1):
        print(source, "-->", i + 1," ------> ", cost[i], "--- ", i+1, "<-", end="")
        temp = i
        while(previous[temp] != 0):
            print(previous[temp] + 1, "<-", end="")
            temp = previous[temp]
        print(source) 

if __name__ == "__main__":
    main()
