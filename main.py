import pygame
import pygame_widgets
import copy
import heapq
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.toggle import Toggle
from BFS import *
from AStar import *
from Greedy import *

"""" 
This is the main file of this interactive. It works by utilizing pygame's
while running structure for the body so the game will always be running. We start
by intiliazing all the variables we use, such as the heap, the dropdown, the buttons,
and everything else we use. We then have an if statement (which runs continuously
because of the while running) which cases on whether the user has started the
experience. If not, we are free to take and place the start, end, and obstacle
blocks. We are also ready to accept input from the algorithm dropdown. If the
experience has started, then we want to pause all user input and run the desired
pathfinding algorithm. Once it is done running, the application will return the
path said algorithm took and draw it for the user. The user has access to
3 buttons: Start/pause, clear walls, and reset. Reset will only be visible when the 
game has been paused, and will disappear when the game is over. When this happens,
Start will become reset.
Features that can be added going forward:
- stopping the algorithm if I know it is impossible or after a timer threshold
- more algorithms
- customizable algorithms (i.e. using euclidean instead of manhattan)



By: Davis Germain <dgermain@andrew.cmu.edu>
"""


WIDTH = 1200
HEIGHT = 800
FOURFIFTHWIDTH = (4*WIDTH)/5
FPS = 60

def pygame_init():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Interactive")
    return screen

def set_grid(screen):
    for colLine in range(WIDTH//50):
        pygame.draw.line(screen, (255,255,255), (colLine*50, 0), (colLine*50, HEIGHT))
    for rowLine in range(HEIGHT//50):
        pygame.draw.line(screen, (255,255,255), (0, rowLine*50), (WIDTH, rowLine*50))
    pygame.draw.rect(screen, (255,255,255), (950, 0, 250, HEIGHT))

def mouseInBounds(mousePos):
    if(0 <= mousePos[0] and mousePos[0] < 950):
        if(0 <= mousePos[1] and mousePos[1] < 800):
            return True
    return False

def corner(mousePos):
    newX = mousePos[0]
    newY = mousePos[1]
    while newX % 50 != 0:
        newX -= 1
    while newY % 50 != 0:
        newY -= 1
    return (newX,newY)

def set_blocks(events, selected, blockDict):
    for event in events:
        mousePos = pygame.mouse.get_pos()
        if ((event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION)) and 
            mouseInBounds(mousePos) and
            pygame.mouse.get_pressed()[0]):
            
            selectedBlock = corner(mousePos)

            # remove if exists
            for block in blockDict["Obstacle"][:]:
                if block == selectedBlock:
                    blockDict["Obstacle"].remove(selectedBlock)
            if selectedBlock == blockDict["Start"]:
                blockDict["Start"] = []
                blockDict["Frontier"] = []
            if selectedBlock == blockDict["Goal"]:
                blockDict["Goal"] = []

            # add selected type
            if(selected == "Obstacle" and selectedBlock is not blockDict["Goal"]
               and selectedBlock is not blockDict["Start"]):
                blockDict["Obstacle"].append(selectedBlock)
            elif(selected == "Goal" and selectedBlock is not blockDict["Start"]
                 and selectedBlock not in blockDict["Obstacle"]):
                blockDict["Goal"] = selectedBlock
            elif(selected == "Start" and selectedBlock is not blockDict["Goal"]
                 and selectedBlock not in blockDict["Obstacle"]):
                blockDict["Start"] = selectedBlock
                blockDict["Frontier"] = [selectedBlock]

        events = pygame.event.get()

def centerize(path):
    newPath = copy.deepcopy(path)
    for i in range(len(newPath)):
        newPath[i] = (newPath[i][0] + 25, newPath[i][1]+25)
    return newPath

def getPath(blockDict, selectedAlg):
    if(selectedAlg == "A*"):
        return fullAStar(blockDict)
    elif(selectedAlg == "BFS"):
        return fullBFS(blockDict)
    elif(selectedAlg == "Greedy"):
        return fullGreedy(blockDict)

def main():
    screen = pygame_init()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)
    gameStart = False
    gameComplete = False
    paused = False
    wallsLocked = False
    running = True
    elapsed_time = 0

    blockDict = dict()
    blockDict["Start"] = []
    blockDict["Goal"] = []
    blockDict["Obstacle"] = []
    blockDict["Explored"] = []
    blockDict["Frontier"] = []

    startText = "Start"
    path = []
    heap = []
    heapq.heapify(heap)

    gScore = {}
    parent = {}

    def start_game():
        nonlocal gameStart, paused, gameComplete, wallsLocked
        nonlocal startButton, blockDict

        # cannot start unless all set
        if(blockDict["Start"] != [] and
           blockDict["Goal"] != [] and
           algDropDown.getSelected() is not None):

            if gameComplete:
                resetAlgorithmState()
                return 

            # starting for first time
            if not gameStart and not paused:  
                gameStart = True
                wallsLocked = True 
                startButton.setText("Pause")
                algDropDown.disable()
                restartButton.show() 
                return

            # pausing
            if gameStart and not paused:
                paused = True
                gameStart = False
                startButton.setText("Resume")
                return

            # resuming
            if paused:
                paused = False
                gameStart = True
                startButton.setText("Pause") 
                return

    def clear_walls():
        nonlocal blockDict, wallsLocked
        if wallsLocked:
            return
        blockDict["Obstacle"] = []

    def resetAlgorithmState():
        nonlocal blockDict, heap, gScore, parent, path, gameStart, paused, gameComplete, elapsed_time

        blockDict["Explored"] = []
        blockDict["Frontier"] = [blockDict["Start"]] if blockDict["Start"] else []
        heap.clear()
        heapq.heapify(heap)
        gScore.clear()
        parent.clear()
        path = []
        elapsed_time = 0

        # Reset flags to allow re-running
        gameStart = False
        paused = False
        gameComplete = False
        startButton.setText("Start")
        algDropDown.enable()
        restartButton.show()

    def restart():
        nonlocal blockDict, gameStart, gameComplete, paused, path, wallsLocked, elapsed_time
        blockDict["Start"] = []
        blockDict["Goal"] = []
        blockDict["Obstacle"] = []
        blockDict["Explored"] = []
        blockDict["Frontier"] = []
        heap.clear()
        heapq.heapify(heap)
        gScore.clear()
        parent.clear()
        gameStart = False
        gameComplete = False
        paused = False
        wallsLocked = False
        path = []
        elapsed_time = 0

        startButton.setText("Start")
        restartButton.hide()
        algDropDown.enable()

    startButton = Button(screen, 
                         970,
                         (4*HEIGHT)/5+40, 
                         100, 50, 
                         text = startText, 
                         inactiveColour = (179,179,179),
                         pressedColour = (160,160,160), 
                         onClick = start_game
                         )

    clearWallsButton = Button(screen, 
                         1080,
                         (4*HEIGHT)/5+40, 
                         100, 50, 
                         text = "Clear Walls", 
                         inactiveColour = (179,179,179),
                         pressedColour = (160,160,160), 
                         onClick = clear_walls
                         )
    
    restartButton = Button(screen,
                           1025,(4*HEIGHT)/5+100,
                           100,50,
                           text = "Restart",
                           inactiveColour = (179,179,179),
                           pressedColour = (160,160,160), 
                           onClick = restart
                           )
    restartButton.hide()

    blockDropDown = Dropdown(screen,
                             970,
                             25, 100,
                             50,
                             name = "Block Type",
                             choices = ["Start", "Goal", "Obstacle"],
                             values = ["Start", "Goal", "Obstacle"])

    algDropDown = Dropdown(screen,
                             1080,
                             25, 100,
                             50,
                             name = "Algorithm",
                             choices = ["BFS", "A*", "Greedy"],
                             values = ["BFS", "A*", "Greedy"])

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0,0,0))
        set_grid(screen)

        # Placement of blocks only if not running
        if not gameStart and not paused and not gameComplete:
            set_blocks(events, blockDropDown.getSelected(), blockDict)

        # Animation step
        elif gameStart and not paused:
            alg = algDropDown.getSelected()
            if alg == "BFS":
                result = BFSRound(blockDict, parent)
                if result == "GOAL":
                    gameStart = False
                    paused = False
                    gameComplete = True
                    startButton.setText("Restart")
                    restartButton.hide()
                    path = reconstruct_path(parent, tuple(blockDict["Start"]), tuple(blockDict["Goal"]))
            elif alg == "A*":
                result = AStarRound(blockDict, heap, gScore, parent)
                if result == "GOAL":
                    gameStart = False
                    paused = False
                    gameComplete = True
                    startButton.setText("Restart")
                    restartButton.hide()
                    path = reconstruct_path(parent, tuple(blockDict["Start"]), tuple(blockDict["Goal"]))
                else:
                    heap, gScore, parent = result
            elif alg == "Greedy":
                result = greedyRound(blockDict, heap, parent)
                if result == "GOAL":
                    gameStart = False
                    paused = False
                    gameComplete = True
                    startButton.setText("Restart")
                    restartButton.hide()
                    path = reconstruct_path(parent, tuple(blockDict["Start"]), tuple(blockDict["Goal"]))
                else:
                    heap, parent = result


        dt = clock.get_time() / 1000  # convert milliseconds to seconds
        if gameStart:  # only count time while algorithm is running
            elapsed_time += dt


        # Drawing code (Explored, Frontier, Start, Goal, Obstacles)
        if blockDict["Explored"]:
            for (x,y) in blockDict["Explored"]:
                pygame.draw.rect(screen, (104,255,104),(x,y,50,50))

        if blockDict["Frontier"]:
            for (x,y) in blockDict["Frontier"]:
                pygame.draw.rect(screen, (250,255,84),(x,y,50,50))

        if blockDict["Goal"]:
            pygame.draw.rect(screen, (0,255,0),(blockDict["Goal"][0], blockDict["Goal"][1],50,50))

        if blockDict["Start"]:
            pygame.draw.rect(screen, (255,0,0),(blockDict["Start"][0], blockDict["Start"][1],50,50))

        for (x,y) in blockDict["Obstacle"]:
            pygame.draw.rect(screen, (220,220,220),(x,y,50,50))
        
        time_text = font.render(f"Time: {elapsed_time:.2f}s", True, (0, 0, 0))
        screen.blit(time_text, (1020, 250))  # adjust position as needed

        # Draw final path
        if path:
            centered = centerize(path)
            for i in range(len(centered)-1):
                pygame.draw.line(screen, (255,255,0), centered[i], centered[i+1], 4)

        pygame_widgets.update(events)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()