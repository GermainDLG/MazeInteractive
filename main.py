import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown

WIDTH = 1200
HEIGHT = 800
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



def main():
    screen = pygame_init()
    clock = pygame.time.Clock()
    running = True

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


        pygame.display.flip()
        clock.tick(FPS)

    
    pygame.quit()



if __name__ == "__main__":
    main()