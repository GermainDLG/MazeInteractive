import pygame
import pygame_widgets
import copy
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.toggle import Toggle
from BFS import *

WIDTH = 1200
HEIGHT = 800
FOURFIFTHWIDTH = (4*WIDTH)/5
FPS = 30

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
    pygame.draw.rect(screen, (255,255,255), (950, 0, 250, HEIGHT)) #x,y,width,height

def mouseInBounds(mousePos):
    if(0 <= mousePos[0] and mousePos[0] < 950):
        if(0 <= mousePos[1] and mousePos[1] < 800): #ONE OFF ERROR FOR LOWEST PIXEL
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
            #add block to list
            for block in blockDict["Obstacle"]:
                if block == selectedBlock:
                    blockDict["Obstacle"].remove(selectedBlock)
            if selectedBlock == blockDict["Start"]:
                blockDict["Start"] = []
                blockDict["Frontier"] = []
            if selectedBlock == blockDict["Goal"]:
                blockDict["Goal"] = []

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
        mousePos = pygame.mouse.get_pos()

def centerize(path):
    newPath = copy.deepcopy(path)
    for i in range(len(newPath)):
        newPath[i] = (newPath[i][0] + 25, newPath[i][1]+25)
    return newPath

def main():
    screen = pygame_init()
    clock = pygame.time.Clock()
    gameStart = False
    gameComplete = False
    running = True
    blockDict = dict()
    blockDict["Start"] = [] #START
    blockDict["Goal"] = [] #GOAL
    blockDict["Obstacle"] = [] #OBSTACLE
    blockDict["Explored"] = []
    blockDict["Frontier"] = []
    startText = "Start"
    path = []
    def start_game():
        nonlocal gameStart, startButton
        nonlocal blockDict
        if(blockDict["Start"] != [] and
           blockDict["Goal"] != [] and
           algDropDown.getSelected() is not None):
            gameStart = not gameStart
            if gameComplete == True:
                startButton.setText("Restart")
                #issue: does not update when someone does not click first
            elif gameStart == True:
                startButton.setText("Pause")
            else:
                startButton.setText("Start")

    def clear_walls():
        nonlocal blockDict
        blockDict["Obstacle"] = []
        gameComplete = False

    def restart():
        nonlocal blockDict
        nonlocal gameStart
        nonlocal gameComplete
        nonlocal path
        blockDict["Start"] = [] #START
        blockDict["Goal"] = [] #GOAL
        blockDict["Obstacle"] = [] #OBSTACLE
        blockDict["Explored"] = []
        blockDict["Frontier"] = []
        gameStart = False
        gameComplete = False
        path = []


    startButton = Button(screen, 
                         970, #excuse the magic numbers
                         (4*HEIGHT)/5+40, 
                         100, 50, 
                         text = startText, 
                         inactiveColour = (179,179,179),
                         pressedColour = (160,160,160), 
                         onClick = start_game
                         )
    
    clearWallsButton = Button(screen, 
                         1080, #excuse the magic numbers
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
                             choices = ["BFS", "DFS", "TDB"],
                             values = ["BFS", "DFS", 3])

    while running:
        #reinitializes the mousepos and event list
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()

        #CODE HERE
        #set grid
        screen.fill((0,0,0))
        set_grid(screen)

        #handles user adding obstacles, goal and start blocks while we have not
        #started
        if(gameStart == False and gameComplete == False):
            set_blocks(events, blockDropDown.getSelected(), blockDict)
        elif(gameStart == True):
            if(algDropDown.getSelected() == "BFS"):
                #run bfs
                BFSRound(blockDict)
        
        if(blockDict["Explored"] != []):
            for i in range(len(blockDict["Explored"])):
                pygame.draw.rect(screen, (104,255,104),
                                 (blockDict["Explored"][i][0],blockDict["Explored"][i][1],
                                  50,50))

        if(blockDict["Frontier"] != []):
            for i in range(len(blockDict["Frontier"])):
                pygame.draw.rect(screen, (250,255,84),
                                 (blockDict["Frontier"][i][0],blockDict["Frontier"][i][1],
                                  50,50))

        if(blockDict["Goal"] != []):
            pygame.draw.rect(screen, (0,255,0), 
                             (blockDict["Goal"][0], blockDict["Goal"][1],
                              50, 50))
        
        if(blockDict["Start"] != []):
            pygame.draw.rect(screen, (255,0,0), 
                             (blockDict["Start"][0], blockDict["Start"][1],
                              50, 50))
        
        if(blockDict["Obstacle"] != []):
            for i in range(len(blockDict["Obstacle"])):
                pygame.draw.rect(screen, (220,220,220),
                                 (blockDict["Obstacle"][i][0],blockDict["Obstacle"][i][1],
                                  50,50))

        if(path != []):
            path = centerize(path)
            for i in range(len(path)):
                if(i+1 != len(path)):
                    pygame.draw.line(screen, (255,255,0), path[i], path[i+1], 4)        
        #TO HERE

        pygame_widgets.update(events)
        pygame.display.flip()
        clock.tick(FPS)

        for (existingX, existingY) in blockDict["Explored"]:
            if (existingX, existingY) == blockDict["Goal"]:
                gameStart = False
                gameComplete = True
                startButton.setText("Restart")
                path = fullBFS(blockDict)





if __name__ == "__main__":
    main()