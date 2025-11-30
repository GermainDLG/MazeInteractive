import heapq

def inBounds(x, y):
    return 0 <= x < 950 and 0 <= y < 800

def h(coord, blockDict):
    """Manhattan distance heuristic for greedy search (admissible for 4-way grid)"""
    gx, gy = blockDict["Goal"]
    x, y = coord
    return abs(x - gx) + abs(y - gy)

def GreedyRound(blockDict, heap, parent):
    """
    One step of Greedy Best-First Search animation.
    Returns:
        - "GOAL" if the goal is reached
        - Otherwise, updated heap and parent
    """
    directions = [(-50,0), (50,0), (0,-50), (0,50)]

    # initialize
    if not heap:
        start = tuple(blockDict["Start"])
        heapq.heappush(heap, (h(start, blockDict), start))
        if start not in blockDict["Frontier"]:
            blockDict["Frontier"].append(start)
        return heap, parent

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

        if neighbor not in parent:  # visit each neighbor once
            parent[neighbor] = current
            heapq.heappush(heap, (h(neighbor, blockDict), neighbor))
            if neighbor not in blockDict["Frontier"]:
                blockDict["Frontier"].append(neighbor)

    return heap, parent

def reconstruct_path(parent, start, end):
    """Reconstruct path from parent mapping."""
    path = [end]
    current = end
    while current != start:
        current = parent.get(current)
        if current is None:
            return None
        path.append(current)
    path.reverse()
    return path

def fullGreedy(blockDict):
    """Compute full greedy path from start to goal."""
    start = tuple(blockDict["Start"])
    goal = tuple(blockDict["Goal"])
    heap = []
    parent = {}
    heapq.heappush(heap, (h(start, blockDict), start))
    explored = set()

    directions = [(-50,0), (50,0), (0,-50), (0,50)]

    while heap:
        f_val, current = heapq.heappop(heap)
        explored.add(current)

        if current == goal:
            return reconstruct_path(parent, start, goal)

        cx, cy = current
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            neighbor = (nx, ny)
            if 0 <= nx < 950 and 0 <= ny < 800 and neighbor not in blockDict["Obstacle"]:
                if neighbor not in parent and neighbor not in explored:
                    parent[neighbor] = current
                    heapq.heappush(heap, (h(neighbor, blockDict), neighbor))

    return None