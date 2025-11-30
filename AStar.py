import heapq


"""" 
This is my implementation of A*. It works very similarly to greedy. It creates
a priority queue starting with the start node, and appends each surrounding block
in the 4 directions to the priority queue. It then checks if any of these are
the goal node, and if they are not, it either returns having completed its 
iteration (AStarRound), or it loops again until the heap is empty (fullAStar).
The heuristic here is also absolute distance from the goal node, except we also
store a "gscore" for each node, which is the number of steps taken to get there
from the start node.


By: Davis Germain <dgermain@andrew.cmu.edu>
"""

GRID_SIZE = 50  #block size

def inBounds(x, y):
    return 0 <= x < 950 and 0 <= y < 800

def h(coord, blockDict):
    gx, gy = blockDict["Goal"]
    x, y = coord
    return (abs(x - gx) // GRID_SIZE) + (abs(y - gy) // GRID_SIZE)

def AStarRound(blockDict, heap, gScore, parent):
    directions = [(-GRID_SIZE,0), (GRID_SIZE,0), (0,-GRID_SIZE), (0,GRID_SIZE)]
    
    if not heap:
        start = tuple(blockDict["Start"])
        gScore[start] = 0
        heapq.heappush(heap, (h(start, blockDict), start))
        if start not in blockDict["Frontier"]:
            blockDict["Frontier"].append(start)
        return heap, gScore, parent

    current = (heapq.heappop(heap))[1]

    if current in blockDict["Frontier"]:
        try:
            blockDict["Frontier"].remove(current)
        except ValueError:
            pass

    if current not in blockDict["Explored"]:
        blockDict["Explored"].append(current)

    if current == tuple(blockDict["Goal"]):
        return "GOAL"

    cx, cy = current
    for dx, dy in directions:
        nx, ny = cx + dx, cy + dy
        neighbor = (nx, ny)

        if not inBounds(nx, ny) or neighbor in blockDict["Obstacle"]:
            continue

        tentative_g = gScore[current] + 1  # one step per grid

        if tentative_g < gScore.get(neighbor, float('inf')):
            parent[neighbor] = current
            gScore[neighbor] = tentative_g
            fscore = tentative_g + h(neighbor, blockDict)
            heapq.heappush(heap, (fscore, neighbor))

            if neighbor not in blockDict["Frontier"]:
                blockDict["Frontier"].append(neighbor)

    return heap, gScore, parent

def reconstruct_path(parent, end):
    path = [end]
    while end in parent:
        end = parent[end]
        path.append(end)
    path.reverse()
    return path

def fullAStar(blockDict):
    start = tuple(blockDict["Start"])
    goal = tuple(blockDict["Goal"])
    directions = [(-GRID_SIZE,0), (GRID_SIZE,0), (0,-GRID_SIZE), (0,GRID_SIZE)]

    heap = []
    gScore = {start: 0}
    parent = {}
    heapq.heappush(heap, (h(start, blockDict), start))

    while heap:
        current = (heapq.heappop(heap))[1]

        if current == goal:
            return reconstruct_path(parent, goal)

        cx, cy = current
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            neighbor = (nx, ny)

            if not inBounds(nx, ny) or neighbor in blockDict["Obstacle"]:
                continue

            tentative_g = gScore[current] + 1

            if tentative_g < gScore.get(neighbor, float('inf')):
                parent[neighbor] = current
                gScore[neighbor] = tentative_g
                heapq.heappush(heap, (tentative_g + h(neighbor, blockDict), neighbor))

    return None