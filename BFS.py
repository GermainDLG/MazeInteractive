import copy
from main import *
from collections import deque


def inBounds(x,y):
    if(0 <= x and x < 950):
        if(0 <= y and y < 800):
            return True
    return False

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

def notInPath(coord, path):
    for pair in path:
        if pair == coord:
            return False
    return True

def isSemiValid(blockDict, coord, path):
    x, y = coord
    if(inBounds(x,y) and 
       isntObstacle(blockDict, x, y) and
       notInPath(coord, path)):
        return True
    return False



def BFSRound(blockDict):
    directions = [(-50,0), (50,0), (0,-50), (0,50)]
    tmpFrontier = copy.deepcopy(blockDict["Frontier"])
    for oldCoord in blockDict["Frontier"]:
        blockDict["Explored"].append(oldCoord)
    blockDict["Frontier"] = []
    for (oldX, oldY) in tmpFrontier:
        for (drow, dcol) in directions:
            newCoord = (oldX+drow, oldY + dcol)
            if(isValid(blockDict, newCoord)):
                blockDict["Frontier"].append(newCoord)

#def fullBFS(blockDict):
    # wrapper that starts with just current position
#    startingPath = []
#    startingPath.append(blockDict["Start"])
#    return BFSWrapper(blockDict, startingPath)


def BFSWrapper(blockDict, path):
    if(path[-1] == blockDict["Goal"]):
        return path
    else:
        directions = [(-50,0), (50,0), (0,-50), (0,50)]
        mostRecent = path[-1]
        for (drow, dcol) in directions:
            newPos = (mostRecent[0] + drow, mostRecent[1] + dcol)
            if(isSemiValid(blockDict, newPos, path)):
                newPath = copy.deepcopy(path)
                newPath.append(newPos)
                return BFSWrapper(blockDict, newPath)

def fullBFS(blockDict):
    start = blockDict["Start"]
    goal = blockDict["Goal"]
    directions = [(-50,0), (50,0), (0,-50), (0,50)]

    queue = deque()
    queue.append([start])
    visited = set([start])

    while queue:
        path = queue.popleft()
        r, c = path[-1]

        if (r, c) == goal:
            return path

        for dr, dc in directions:
            newPos = (r + dr, c + dc)
            if isSemiValid(blockDict, newPos, path) and newPos not in visited:
                visited.add(newPos)
                newPath = path + [newPos]
                queue.append(newPath)

    return None