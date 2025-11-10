import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown

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




def main():
    screen = pygame_init()
    clock = pygame.time.Clock()
    gameStart = False
    running = True

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
                             values = [1, 2, 3])

    algDropDown = Dropdown(screen,
                             1080,
                             25, 100,
                             50,
                             name = "Algorithm",
                             choices = ["BFS", "DFS", "TDB"],
                             values = [1, 2, 3])
    

    


    while running:
        events = pygame.event.get()
        mousePos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        #CODE HERE

        screen.fill((0,0,0))
        set_grid(screen)


        #TO HERE

        pygame_widgets.update(events)
        pygame.display.flip()
        clock.tick(FPS)

    
    pygame.quit()



if __name__ == "__main__":
    main()