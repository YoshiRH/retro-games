import pygame
import os

def main(root):

    #Initialize game and embed it in the Tkinter Window
    pygame.init()
    os.environ['SDL_WINDOWID'] = str(root.winfo_id())
    pygame.display.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    #Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill("#D3E671")

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()