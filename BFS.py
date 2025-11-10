import copy
from main import *


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

def isValid(blockDict, coord):
    x, y = coord
    if(inBounds(x,y) and 
       isntExplored(blockDict, x, y) and 
       isntObstacle(blockDict, x, y)):
        return True
    return False



def BFSRound(blockDict):
    directions = [(-50,0), (50,0), (0,-50), (0,50)]
    for oldCoord in blockDict["Frontier"]:
        blockDict["Explored"].append(oldCoord)
    blockDict["Frontier"] = []
    for (oldX, oldY) in blockDict["Explored"]:
        for (drow, dcol) in directions:
            newCoord = (oldX+drow, oldY + dcol)
            if(isValid(blockDict, newCoord)):
                blockDict["Frontier"].append(newCoord)
