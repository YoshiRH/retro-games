import pygame, os, random
from pygame.math import Vector2
from .in_game_menu import InGameMenu

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

    def try_change_direction(self, new_direction):
        if not self.body[0] + new_direction == self.body[1]:
            self.direction = new_direction

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

    def reposition(self, snake):
        self.position = Vector2(random.randint(0, game_board_grid_size_x - 1),
                                random.randint(0, game_board_grid_size_y - 1))
        for coordinates in snake.body:
            if coordinates == self.position:
                self.reposition(snake)

class Game:
    def __init__(self):
        self.apple = Apple()
        self.snake = Snake()
        self.running = True
        self.hit_sound = pygame.mixer.Sound('media/snake/hit.wav')
        self.hit_sound.set_volume(0.40)
        self.eat_sound = pygame.mixer.Sound('media/snake/eat.wav')
        self.eat_sound.set_volume(0.40)
        self.end_pop_up = pygame.image.load('media/snake/endPopUp.png').convert_alpha()

    def update_logic(self):
        if self.running:
            self.check_self_collision()
            self.check_border_collision()
            self.try_eating_apple()
            if self.running:
                self.snake.move()

    def draw_objects(self, screen):
        self.apple.draw(screen)
        self.snake.draw(screen)
        self.draw_score(screen)
        if not self.running:
            self.draw_end_screen(screen)

    def try_eating_apple(self):
        if self.apple.position == self.snake.body[0]:
            self.snake.grow = True
            self.eat_sound.play()
            self.apple.reposition(self.snake)

    def check_self_collision(self):
        upcoming_position = self.snake.body[0] + self.snake.direction
        for coordinates in self.snake.body:
            if upcoming_position == coordinates:
                self.fail()

    def check_border_collision(self):
        upcoming_position = self.snake.body[0] + self.snake.direction
        if upcoming_position.x < 0 or upcoming_position.x > game_board_grid_size_x - 1:
            self.fail()
        if upcoming_position.y < 0 or upcoming_position.y > game_board_grid_size_y - 1:
            self.fail()

    def fail(self):
        self.running = False
        self.hit_sound.play()

    def draw_score(self, screen):
        score_border = pygame.Rect(314, 14, 169, 84)
        font = pygame.font.Font('media/snake/VT323-Regular.ttf', 110)
        score = str(len(self.snake.body) - 3)
        score_rectangle = pygame.Rect(330, 0, 174, 70)
        score_surface = font.render(score, True, '#d3e671')

        pygame.draw.rect(screen, "#4d6127", score_border)
        screen.blit(score_surface, score_rectangle)

    def draw_end_screen(self, screen):
        rectangle = pygame.Rect(139, 180, 525, 350)
        screen.blit(self.end_pop_up, rectangle)

def main(root):

    #Initialization and embed inside the Tkinter Window
    pygame.init()
    os.environ['SDL_WINDOWID'] = str(root.winfo_id())
    pygame.display.init()
    screen = pygame.display.set_mode((800,600))
    clock = pygame.time.Clock()
    game = Game()
    menu = InGameMenu(screen)

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
                    case pygame.K_r:
                        game = Game()
                    case pygame.K_p:
                        menu.toggle()
                    case pygame.K_w:
                        game.snake.try_change_direction(Vector2(0,-1))
                    case pygame.K_s:
                        game.snake.try_change_direction(Vector2(0, 1))
                    case pygame.K_d:
                        game.snake.try_change_direction(Vector2(1, 0))
                    case pygame.K_a:
                        game.snake.try_change_direction(Vector2(-1, 0))
            if event.type == SCREEN_UPDATE and not menu.active:
                game.update_logic()

        screen.fill("#89ac46")
        draw_game_board(screen)
        game.draw_objects(screen)

        menu.draw()

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