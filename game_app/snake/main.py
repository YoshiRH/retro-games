import pygame, os
from pygame.math import Vector2
from .in_game_menu import InGameMenu, MenuType
from .additional import draw_game_board
from .snake import Snake, Apple

element_size = 35
grid_size_x = 21
grid_size_y = 12
game_board_loc_x = 34
game_board_loc_y = 145

primary_color = "#89ac46"
secondary_color = "#4d6127"
highlight_color = "#d3e671"
hover_color = "#889a66"

class Game:
    def __init__(self, screen):
        self.apple = Apple(element_size, grid_size_x, grid_size_y, game_board_loc_x, game_board_loc_y)
        self.snake = Snake(element_size, game_board_loc_x, game_board_loc_y)
        self.running = True
        self.hit_sound = pygame.mixer.Sound('media/snake/hit.wav')
        self.hit_sound.set_volume(0.40)
        self.eat_sound = pygame.mixer.Sound('media/snake/eat.wav')
        self.eat_sound.set_volume(0.40)
        #todo Cleanup temporary code later
        self.menu = InGameMenu(screen, 139, 180, primary_color, secondary_color, highlight_color, hover_color)

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

    def try_eating_apple(self):
        if self.apple.position == self.snake.body[0]:
            self.snake.grow = True
            self.eat_sound.play()
            self.apple.reposition(self.snake)
        if len(self.snake.body) - 3 >= 245:
            self.running = False
            self.menu.enable_menu(MenuType.WIN)

    def check_self_collision(self):
        upcoming_position = self.snake.body[0] + self.snake.direction
        for coordinates in self.snake.body:
            if upcoming_position == coordinates:
                self.fail()

    def check_border_collision(self):
        upcoming_position = self.snake.body[0] + self.snake.direction
        if upcoming_position.x < 0 or upcoming_position.x > grid_size_x - 1:
            self.fail()
        if upcoming_position.y < 0 or upcoming_position.y > grid_size_y - 1:
            self.fail()

    def fail(self):
        self.running = False
        self.hit_sound.play()
        self.menu.enable_menu(MenuType.LOSS)

    def draw_score(self, screen):
        score_border = pygame.Rect(314, 14, 169, 84)
        font = pygame.font.Font('media/snake/Jersey25-Regular.ttf', 95)
        score = str(len(self.snake.body) - 3)
        score_surface = font.render(score, True, '#d3e671')
        score_rectangle = score_surface.get_rect(center=score_border.center)

        pygame.draw.rect(screen, "#4d6127", score_border)
        screen.blit(score_surface, score_rectangle)

    def get_game_speed(self):
        score = len(self.snake.body) - 3
        speed = 200 - (score * 5)
        if speed < 120:
            return 120
        else:
            return speed

def main(root):
    # Initialization and embed inside the Tkinter Window
    pygame.mixer.pre_init(44100, -16, 2, 64)
    pygame.mixer.init()
    pygame.init()
    os.environ['SDL_WINDOWID'] = str(root.winfo_id())
    pygame.display.init()
    screen = pygame.display.set_mode((800,600))
    clock = pygame.time.Clock()
    game = Game(screen)
    #menu = InGameMenu(screen, 139, 180, "#89ac46", "#4d6127", "#d3e671")

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 120)

    game.menu.enable_menu(MenuType.START)

    #Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        if not game.menu.active:
                            game.menu.enable_menu(MenuType.PAUSE)
                        else:
                            game.menu.active = False
                    case pygame.K_r:
                        game = Game(screen)
                    case pygame.K_w:
                        game.snake.try_change_direction(Vector2(0,-1))
                    case pygame.K_s:
                        game.snake.try_change_direction(Vector2(0, 1))
                    case pygame.K_d:
                        game.snake.try_change_direction(Vector2(1, 0))
                    case pygame.K_a:
                        game.snake.try_change_direction(Vector2(-1, 0))
            if game.menu.active:
                result = game.menu.handle_event(event)
                if result == "quit":
                    running = False
                elif result == "continue":
                    game.menu.disable()
                elif result == "retry":
                    game = Game(screen)
                elif result == "start":
                    game.menu.disable()
            if event.type == SCREEN_UPDATE and not game.menu.active:
                pygame.time.set_timer(SCREEN_UPDATE, game.get_game_speed())
                game.update_logic()
        screen.fill("#89ac46")
        draw_game_board(screen, element_size, grid_size_x, grid_size_y, game_board_loc_x, game_board_loc_y, primary_color, secondary_color, highlight_color)
        game.draw_objects(screen)

        game.menu.draw_current(len(game.snake.body) - 3)

        pygame.display.update()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()