from main import *

def printGrid(grid):
    for i in range(18):
        print(grid[i])

def setGrid():
    wholeMap = []
    #32x18
    for i in range(18):
        wholeMap.append([])
        for j in range(32):
            wholeMap[i].append(0)
    print(wholeMap)
    return wholeMap

def BFSRound(grid):
    pass
    #essentially just do one round of bfs homeslice, and return a bool gang