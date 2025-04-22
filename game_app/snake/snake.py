import pygame, os, random
from pygame.math import Vector2

game_board_element_size = 35
game_board_grid_size_x = 21
game_board_grid_size_y = 12
game_board_x = 34
game_board_y = 145

class Snake:
    def __init__(self):
        self.body = [Vector2(3,6),Vector2(4,6),Vector2(5,6)]
        self.direction = Vector2(1,0)

    def draw(self, screen):
        for coordinates in self.body:
            snake_body_part = pygame.Rect(game_board_x + (coordinates.x * game_board_element_size),
                            game_board_y + (coordinates.y * game_board_element_size)
                            , game_board_element_size, game_board_element_size)
            pygame.draw.rect(screen, "#305CDE", snake_body_part)

    def move(self):
        self.body.pop()
        self.body.insert(0, self.body[0] + self.direction)

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
    snake = Snake()

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 120)

    #Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        running = False
                    case pygame.K_w:
                        snake.direction = Vector2(0,-1)
                    case pygame.K_s:
                        snake.direction = Vector2(0, 1)
                    case pygame.K_d:
                        snake.direction = Vector2(1, 0)
                    case pygame.K_a:
                        snake.direction = Vector2(-1, 0)
            if event.type == SCREEN_UPDATE:
                snake.move()

        screen.fill("#89ac46")
        pygame.draw.rect(screen, "#4d6127", game_board_border)
        pygame.draw.rect(screen, "#d3e671", game_board)
        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()