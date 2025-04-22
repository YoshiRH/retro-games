import pygame
import os

def main(root):

    #Initialize game and embed it in the Tkinter Window
    pygame.init()
    os.environ['SDL_WINDOWID'] = str(root.winfo_id())
    pygame.display.init()
    screen = pygame.display.set_mode((800,600))
    clock = pygame.time.Clock()

    grid_box_size = 35

    game_board_border = pygame.Rect(0,112,800,488)
    game_board = pygame.Rect(34, 145, (21 * grid_box_size), (12 * grid_box_size))

    #Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill("#89ac46")
        pygame.draw.rect(screen, "#4d6127", game_board_border)
        pygame.draw.rect(screen, "#d3e671", game_board)

        pygame.display.update()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()