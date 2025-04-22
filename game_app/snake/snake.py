import pygame, os, random

game_board_element_size = 35
game_board_grid_size_x = 21
game_board_grid_size_y = 12
game_board_x = 34
game_board_y = 145

class Apple:
    def __init__(self):
        self.x = random.randint(0, game_board_grid_size_x - 1)
        self.y = random.randint(0, game_board_grid_size_y - 1)

    def draw(self, screen):
        apple = pygame.Rect(game_board_x + (self.x * game_board_element_size),
                            game_board_y + (self.y * game_board_element_size)
                            , game_board_element_size, game_board_element_size)
        pygame.draw.rect(screen, "#C7372F", apple)

def main(root):

    #Initialization and embed inside the Tkinter Window
    pygame.init()
    os.environ['SDL_WINDOWID'] = str(root.winfo_id())
    pygame.display.init()
    screen = pygame.display.set_mode((800,600))
    clock = pygame.time.Clock()

    #Game objects
    game_board_border = pygame.Rect(0,112,800,488)
    game_board = pygame.Rect(game_board_x, game_board_y,
                             (game_board_grid_size_x * game_board_element_size),
                             (game_board_grid_size_y * game_board_element_size))
    apple = Apple()

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
        apple.draw(screen)

        pygame.display.update()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()