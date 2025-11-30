from main import *
import heapq

def isntExplored(blockDict, x,y):
    for (existingX, existingY) in blockDict["Explored"]:
        if (existingX, existingY) == (x,y):
            return False
    return True

def isntObstacle(blockDict, x,y):
    for (existingX, existingY) in blockDict["Obstacle"]:
        if (existingX, existingY) == (x,y):
            return False
    return True

def isntInFrontier(blockDict, x, y):
    for (existingX, existingY) in blockDict["Frontier"]:
        if((existingX, existingY) == (x,y)):
            return False
    return True

def isValid(blockDict, coord):
    x, y = coord
    if(inBounds(x,y) and 
       isntExplored(blockDict, x, y) and 
       isntObstacle(blockDict, x, y) and
       isntInFrontier(blockDict, x, y)):
        return True
    return False

def inBounds(x,y):
    if(0 <= x and x < 950):
        if(0 <= y and y < 800):
            return True
    return False

def h(coord, blockDict):
    coordX, coordY = coord
    return abs(coordX - blockDict["Goal"][0]) + abs(coordY - blockDict["Goal"][1])

def g(coord, blockDict):
    coordX, coordY = coord
    return abs(coordX - blockDict["Start"][0]) + abs(coordY - blockDict["Start"][1])

def f(coord, blockDict):
    return h(coord, blockDict) #g(coord, blockDict) + 

def AStarRound(blockDict, heap):
    visited = set(blockDict["Explored"])
    directions = [(-50,0), (50,0), (0,-50), (0,50)]
    if(heap == []):
        heapq.heappush(heap, (f(blockDict["Start"], blockDict), blockDict["Start"]))
    #here
    exploreHere = (heapq.heappop(heap))[1]
    blockDict["Frontier"].remove(exploreHere)
    blockDict["Explored"].append(exploreHere)
    r,c = exploreHere
    for dr, dc in directions:
            newPos = (r + dr, c + dc)
            if(newPos not in visited): 
                if(isValid(blockDict, newPos)):
                    heapq.heappush(heap, (f(newPos, blockDict), newPos))
                    if(inBounds(newPos[0], newPos[1])):
                        blockDict["Frontier"].append(newPos)
    return heap

def fullAStar(blockDict):
    heap = []
    heapq.heapify(heap)
    directions = [(-50,0), (50,0), (0,-50), (0,50)]
    heapq.heappush(heap, (f(blockDict["Start"], blockDict), blockDict["Start"]))
    visited = set()

    return