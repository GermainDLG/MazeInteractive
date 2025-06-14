import copy
from main import *

def isInBounds(row, col):
    if (row < 0) or (row > 17):
        return False
    if (col < 0) or (col > 31):
        return False
    return True

def isUndiscovered(row,col):
    if (dataDict["wholeGrid"][row][col] == 0) or (dataDict["wholeGrid"][row][col] == 3):
        return True
    return False

def isValid(row, col):
    if (isInBounds(row,col) and isUndiscovered(row, col)):
        return True
    return False


def BFSRound():
    directions = [(1,0),(-1,0),(0,1),(0,-1)]
    tempGrid = copy.deepcopy(dataDict["wholeGrid"])


    for row in range(18): #for each row
        for col in range(32): # and each value in each row
            if tempGrid[row][col] == 2: #if the value is on the frontier
                #check up, add up, check left, add left, etc.
                for direction in directions:
                    deltaRow, deltaCol = direction
                    newRow = row + deltaRow
                    newCol = col + deltaCol
                    if(isValid(newRow, newCol)):
                        #check if goal, otherwise set to 1 and move on
                        if dataDict["wholeGrid"][newRow][newCol] == 3:
                            return True
                        else:
                            dataDict["wholeGrid"][newRow][newCol] = 2 #set it to the explored
                            dataDict["wholeGrid"][row][col] = 1

                
                
    #essentially just do one round of bfs homeslice, and return a bool gang
    pass