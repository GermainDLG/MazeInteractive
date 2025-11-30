import copy
from collections import deque

"""" 
This is my implementation of BFS for my pathfinding interactive. It works with
BFSRound, which will run one iteration of BFS, and fullBFS, which will run the
whole search algorithm. BFSRound will take every node in the frontier, set it
to explored in blockDict, and then check all 4 directions (up, down, left, right),
and add those positions to the frontier if they are valid (i.e. in bounds, have
not been explored, are not an obstacle, and are not already in the frontier.)
There is also FullBFS which completes the same action, however it has a while
loop over the frontier to check if it is empty. While it is not empty and we
have not found the goal, we keep expanding outwards.

By: Davis Germain <dgermain@andrew.cmu.edu>
"""

def inBounds(x,y):
    return 0 <= x < 950 and 0 <= y < 800

def isntExplored(blockDict, x,y):
    return (x,y) not in blockDict["Explored"]

def isntObstacle(blockDict, x,y):
    return (x,y) not in blockDict["Obstacle"]

def isntInFrontier(blockDict, x, y):
    return (x,y) not in blockDict["Frontier"]

def isValid(blockDict, coord):
    x, y = coord
    return (inBounds(x,y) and isntExplored(blockDict, x,y) 
            and isntObstacle(blockDict, x,y) and isntInFrontier(blockDict, x,y))

def BFSRound(blockDict, parent=None):
    directions = [(-50,0), (50,0), (0,-50), (0,50)]
    tmpFrontier = copy.deepcopy(blockDict["Frontier"])
    blockDict["Frontier"] = []

    for oldCoord in tmpFrontier:
        blockDict["Explored"].append(oldCoord)

        # Check if we reached the goal
        if oldCoord == tuple(blockDict["Goal"]):
            return "GOAL"

        for dr, dc in directions:
            newCoord = (oldCoord[0]+dr, oldCoord[1]+dc)
            if isValid(blockDict, newCoord):
                blockDict["Frontier"].append(newCoord)
                if parent is not None:
                    parent[newCoord] = oldCoord  # track BFS path

    return blockDict["Frontier"] if blockDict["Frontier"] else None

def reconstruct_path(parent, start, goal):
    path = [goal]
    current = goal
    while current != start:
        current = parent.get(current)
        if current is None:
            return None  # no path found
        path.append(current)
    path.reverse()
    return path

def fullBFS(blockDict):
    start = tuple(blockDict["Start"])
    goal = tuple(blockDict["Goal"])
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
            if (inBounds(*newPos) and newPos not in visited and newPos not in blockDict["Obstacle"]):
                visited.add(newPos)
                newPath = path + [newPos]
                queue.append(newPath)

    return None