import pygame_widgets
import pygame
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown

# pygame setup
pygame.init()

def setGrid():
    #32x18
    wholeMap = []
    for i in range(18):
        wholeMap.append([])
        for j in range(32):
            wholeMap[i].append(0)
    print(wholeMap)
    return wholeMap

WIDTH = 1900
HEIGHT = 900

screen = pygame.display.set_mode((WIDTH, HEIGHT))
dataDict = {"obstacles": [], 
            "startBlock": tuple(), 
            "goalBlock": tuple(), 
            "wholeGrid": []}
dataDict["wholeGrid"] = setGrid()
#0s are empty
#1s are explored
#2s are frontier
#3 is goal

blockDropDown = Dropdown(
    screen, 1625, 25,100,40,name="Block Type",
    choices = ["Wall", "Start", "Goal"],
    values = ["Wall", "Start", "Goal"],direction = "down"
)

algDropDown = Dropdown(
    screen, 1775, 25,100,40,name="Algorithm",
    choices = ["BFS", "Alg2", "Alg3"],
    values = ["BFS", "2", "3"],direction = "down"
)

running = True
algorithming = False

def start():
    algorithming = not algorithming

startButton = Button(screen, 1625, 775, 100, 40, text="Start", fontSize = 15,
                     inactiveColour=(150,150,150), hoverColour=(120,120,120),
                     pressedColour=(90,90,9))

def printGrid(grid):
    for i in range(18):
        print(grid[i])

def cornered(coordTuple):
    newX, newY = coordTuple
    while newX % 50 != 0:
        newX -= 1
    while newY % 50 != 0:
        newY -= 1
    return newX,newY

def assignVal(x, y, dropdown):
    if(dropdown == "Wall"):
        if (x,y) not in dataDict["obstacles"]:
            dataDict["obstacles"].append((x,y))
        else:
            dataDict["obstacles"].remove((x,y))
    elif(dropdown == "Start"):
        dataDict["startBlock"] = (x,y)
    elif(dropdown == "Goal"):
        dataDict["goalBlock"] = (x,y)



while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    events = pygame.event.get()
    mousePos = pygame.mouse.get_pos()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif (event.type == pygame.MOUSEBUTTONDOWN) and (mousePos[0] < 1600):
            actualX, actualY = cornered(mousePos)
            assignVal(actualX, actualY, blockDropDown.getSelected())

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("Black")

    # RENDER YOUR GAME HERE
    for i in range(1,18):
        pygame.draw.line(screen, (179,179,179),(0,50*i),(WIDTH,50*i),1)
    for i in range(1,38):
        pygame.draw.line(screen, (179,179,179),(50*i,0),(50*i,WIDTH),1)
    pygame.draw.rect(screen,(255,255,255),pygame.Rect(1600, 0, 300, HEIGHT))
    if(dataDict["goalBlock"]) != tuple():
        pygame.draw.rect(screen,(0,255,0),
                         pygame.Rect(dataDict["goalBlock"][0],
                                     dataDict["goalBlock"][1],51,51))
    if(dataDict["startBlock"]) != tuple():
        pygame.draw.rect(screen,(255,0,0),
                         pygame.Rect(dataDict["startBlock"][0],
                                     dataDict["startBlock"][1],51,51))
    for pos in dataDict["obstacles"]:
        newX, newY = pos
        pygame.draw.rect(screen,(110,115,113),
                         pygame.Rect(newX, newY,51,51))
    
    #AS SOON AS START BUTTON IS CLICKED, LOCK STARTBLOCK AND GOAL AND SET THOSE TO 3 AND 4 RESPECTIVELY

    pygame_widgets.update(events)
    pygame.display.update()

pygame.quit()