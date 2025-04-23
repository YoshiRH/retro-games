import pygame, os, random
from pygame.math import Vector2

game_board_element_size = 35
game_board_grid_size_x = 21
game_board_grid_size_y = 12
game_board_x = 34
game_board_y = 145

class Snake:
    def __init__(self):
        self.body = [Vector2(5,6),Vector2(4,6),Vector2(3,6)]
        self.direction = Vector2(1,0)
        self.grow = False
        self.body_sprite = pygame.image.load('media/snake/body.png').convert_alpha()
        self.head_sprite = pygame.image.load('media/snake/head.png').convert_alpha()
        self.tail_sprite = pygame.image.load('media/snake/tail.png').convert_alpha()
        self.turn_sprite = pygame.image.load('media/snake/turn.png').convert_alpha()

    def draw(self, screen):
        for index, coordinates in enumerate(self.body):
            rectangle = pygame.Rect(game_board_x + (coordinates.x * game_board_element_size),
                                game_board_y + (coordinates.y * game_board_element_size)
                                , game_board_element_size, game_board_element_size)
            sprite = None
            if index == 0:
                sprite = self.rotate_head()
                screen.blit(sprite, rectangle)
            elif index == len(self.body) - 1:
                sprite = self.rotate_tail()
                screen.blit(sprite, rectangle)
            else:
                previous_difference = self.body[index + 1] - self.body[index]
                next_difference = self.body[index - 1] - self.body[index]
                if previous_difference.x == next_difference.x:
                    sprite = self.body_sprite
                elif previous_difference.y == next_difference.y:
                    sprite = pygame.transform.rotate(self.body_sprite, 90)
                else:
                    if (previous_difference.x == 1 and next_difference.y == -1 or
                            previous_difference.y == -1 and next_difference.x == 1):
                        sprite = pygame.transform.rotate(self.turn_sprite, 0)
                    elif (previous_difference.x == -1 and next_difference.y == -1 or
                          previous_difference.y == -1 and next_difference.x == -1):
                        sprite = pygame.transform.rotate(self.turn_sprite, 90)
                    elif (previous_difference.x == -1 and next_difference.y == 1 or
                          previous_difference.y == 1 and next_difference.x == -1):
                        sprite = pygame.transform.rotate(self.turn_sprite, 180)
                    elif (previous_difference.x == 1 and next_difference.y == 1 or
                          previous_difference.y == 1 and next_difference.x == 1):
                        sprite = pygame.transform.rotate(self.turn_sprite, 270)
            if sprite is not None:
                screen.blit(sprite, rectangle)
            else:
                pygame.draw.rect(screen, "#F8ED8C", rectangle)

    def rotate_head(self):
        rotation = self.body[1] - self.body[0]
        if rotation == Vector2(0,1):
            return self.head_sprite
        elif rotation == Vector2(1,0):
            return pygame.transform.rotate(self.head_sprite, 90)
        elif rotation == Vector2(0,-1):
            return pygame.transform.rotate(self.head_sprite, 180)
        elif rotation == Vector2(-1,0):
            return pygame.transform.rotate(self.head_sprite, 270)

    def rotate_tail(self):
        rotation = self.body[-2] - self.body[-1]
        if rotation == Vector2(0,1):
            return self.tail_sprite
        elif rotation == Vector2(1,0):
            return pygame.transform.rotate(self.tail_sprite, 90)
        elif rotation == Vector2(0,-1):
            return pygame.transform.rotate(self.tail_sprite, 180)
        elif rotation == Vector2(-1,0):
            return pygame.transform.rotate(self.tail_sprite, 270)

    def move(self):
        if self.grow:
            self.grow = False
        else:
            self.body.pop()
        self.body.insert(0, self.body[0] + self.direction)

class Apple:
    def __init__(self):
        self.position = Vector2(random.randint(0, game_board_grid_size_x - 1),
                                random.randint(0, game_board_grid_size_y - 1))

    def draw(self, screen):
        rectangle = pygame.Rect(game_board_x + (self.position.x * game_board_element_size),
                            game_board_y + (self.position.y * game_board_element_size)
                            , game_board_element_size, game_board_element_size)
        image = pygame.image.load('media/snake/apple.png').convert_alpha()
        screen.blit(image,rectangle)

    def reposition(self):
        self.position = Vector2(random.randint(0, game_board_grid_size_x - 1),
                                random.randint(0, game_board_grid_size_y - 1))

class Game:
    def __init__(self):
        self.apple = Apple()
        self.snake = Snake()
        self.Fail = False

    def update_logic(self):
        self.check_self_collision()
        self.check_border_collision()
        if not self.Fail:
            self.try_eating_apple()
            self.snake.move()

    def draw_objects(self, screen):
        self.apple.draw(screen)
        self.snake.draw(screen)

    def try_eating_apple(self):
        if self.apple.position == self.snake.body[0]:
            self.snake.grow = True
            self.apple.reposition()

    def check_self_collision(self):
        upcoming_position = self.snake.body[0] + self.snake.direction
        for coordinates in self.snake.body:
            if upcoming_position == coordinates:
                self.Fail = True

    def check_border_collision(self):
        upcoming_position = self.snake.body[0] + self.snake.direction
        if upcoming_position.x < 0 or upcoming_position.x > game_board_grid_size_x - 1:
            self.Fail = True
        if upcoming_position.y < 0 or upcoming_position.y > game_board_grid_size_y - 1:
            self.Fail = True

def main(root):

    #Initialization and embed inside the Tkinter Window
    pygame.init()
    os.environ['SDL_WINDOWID'] = str(root.winfo_id())
    pygame.display.init()
    screen = pygame.display.set_mode((800,600))
    clock = pygame.time.Clock()
    game = Game()

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
                        if game.snake.direction != Vector2(0, 1):
                            game.snake.direction = Vector2(0,-1)
                    case pygame.K_s:
                        if game.snake.direction != Vector2(0, -1):
                            game.snake.direction = Vector2(0, 1)
                    case pygame.K_d:
                        if game.snake.direction != Vector2(-1, 0):
                            game.snake.direction = Vector2(1, 0)
                    case pygame.K_a:
                        if game.snake.direction != Vector2(1, 0):
                            game.snake.direction = Vector2(-1, 0)
            if event.type == SCREEN_UPDATE:
                game.update_logic()

        screen.fill("#89ac46")
        draw_game_board(screen)
        game.draw_objects(screen)

        pygame.display.update()
        clock.tick(60)
    pygame.quit()

def draw_game_board(screen):
    game_board_border = pygame.Rect(0, 112, 800, 488)
    game_board = pygame.Rect(game_board_x, game_board_y,
                             (game_board_grid_size_x * game_board_element_size),
                             (game_board_grid_size_y * game_board_element_size))
    pygame.draw.rect(screen, "#4d6127", game_board_border)
    pygame.draw.rect(screen, "#d3e671", game_board)
    for y in range (game_board_grid_size_y):
        for x in range(game_board_grid_size_x):
            if y % 2 == 0:
                if x % 2 == 0:
                    rectangle = pygame.Rect(game_board_x + (x * game_board_element_size),
                                            game_board_y + (y * game_board_element_size)
                                            , game_board_element_size, game_board_element_size)
                    pygame.draw.rect(screen, "#89AC46", rectangle)
            else:
                if x % 2 == 1:
                    rectangle = pygame.Rect(game_board_x + (x * game_board_element_size),
                                            game_board_y + (y * game_board_element_size)
                                            , game_board_element_size, game_board_element_size)
                    pygame.draw.rect(screen, "#89AC46", rectangle)

if __name__ == "__main__":
    main()