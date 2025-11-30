import copy
from collections import deque

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
    """
    One step of BFS animation.
    Returns:
        - 'GOAL' if goal reached
        - Otherwise, updated frontier and parent dictionary
    """
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
    """Reconstruct BFS path from parent mapping."""
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
    """Run full BFS to get complete path from start to goal."""
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