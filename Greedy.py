import heapq

"""" 
This is my implementation of Greedy search. Two main functions make up this file:
greedyRound and fullGreedy
greedyRound starts by taking in the heap (initializing if it does not exist yet),
and then adds the current block to explored. If it is the goal, return "GOAL".
Otherwise, for each direction, we get its weight and add it to the priority queue.
The weights assigned go by the absolute distance from the goal node.

fullGreedy does the exact same thing, except it holds a while loop over the heap.
While the heap is not empty, we keep searching with the same process defined above.
We return None if we cannot find a path (i.e. the pq is empty)

By: Davis Germain <dgermain@andrew.cmu.edu>
"""

def inBounds(x, y):
    return 0 <= x < 950 and 0 <= y < 800

def h(coord, blockDict):
    gx, gy = blockDict["Goal"]
    x, y = coord
    return abs(x - gx) + abs(y - gy)

def greedyRound(blockDict, heap, parent):
    directions = [(-50,0), (50,0), (0,-50), (0,50)]
    # initialize
    if not heap:
        start = tuple(blockDict["Start"])
        heapq.heappush(heap, (h(start, blockDict), start))
        if start not in blockDict["Frontier"]:
            blockDict["Frontier"].append(start)
        return heap, parent

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

        if neighbor not in parent:  # visit each neighbor once
            parent[neighbor] = current
            heapq.heappush(heap, (h(neighbor, blockDict), neighbor))
            if neighbor not in blockDict["Frontier"]:
                blockDict["Frontier"].append(neighbor)

    return heap, parent

def reconstruct_path(parent, start, end):
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
    start = tuple(blockDict["Start"])
    goal = tuple(blockDict["Goal"])
    heap = []
    parent = {}
    heapq.heappush(heap, (h(start, blockDict), start))
    explored = set()

    directions = [(-50,0), (50,0), (0,-50), (0,50)]

    while heap:
        current = heapq.heappop(heap)[1]
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