import heapq

GRID_SIZE = 50  # your block size

def inBounds(x, y):
    return 0 <= x < 950 and 0 <= y < 800

def h(coord, blockDict):
    """Manhattan distance in grid units (admissible for 4-way movement)"""
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

    f_val, current = heapq.heappop(heap)

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
        f_val, current = heapq.heappop(heap)

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