import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
from BFS import *

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

def set_blocks(mousePos, events, selected, blockDict):
    for event in events:
        if ((event.type == pygame.MOUSEBUTTONDOWN) and 
            mouseInBounds(mousePos)):
            selectedBlock = corner(mousePos)
            print({selectedBlock})
            #add block to list
            if(selected == "Obstacle"):
                blockDict["Obstacle"].append(selectedBlock)
            elif(selected == "Goal"):
                blockDict["Goal"] = selectedBlock
            elif(selected == "Start"):
                blockDict["Start"] = selectedBlock
                blockDict["Frontier"] = [selectedBlock]

def main():
    screen = pygame_init()
    clock = pygame.time.Clock()
    gameStart = False
    running = True
    blockDict = dict()
    blockDict["Start"] = [] #START
    blockDict["Goal"] = [] #GOAL
    blockDict["Obstacle"] = [] #OBSTACLE
    blockDict["Explored"] = []
    blockDict["Frontier"] = []

    def start_game():
        nonlocal gameStart
        gameStart = True

    startButton = Button(screen, 
                         1000, #excuse the magic numbers
                         (4*HEIGHT)/5+50, 
                         150, 50, 
                         text = "Start", 
                         inactiveColour = (179,179,179),
                         pressedColour = (160,160,160), 
                         onClick = start_game
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
        mousePos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        #CODE HERE
        #set grid
        screen.fill((0,0,0))
        set_grid(screen)

        #handles user adding obstacles, goal and start blocks while we have not
        #started
        if(gameStart == False):
            set_blocks(mousePos, events, blockDropDown.getSelected(), blockDict)
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
                print({i})
                print({blockDict["Frontier"][i]})
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
        #TO HERE

        pygame_widgets.update(events)
        pygame.display.flip()
        clock.tick(FPS)
        
    pygame.quit()



if __name__ == "__main__":
    main()