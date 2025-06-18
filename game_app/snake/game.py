import pygame
from .snake import Apple, Snake
from .in_game_menu import InGameMenu, MenuType
from .game_config import GameConfig

class Game:
    def __init__(self, screen, config: GameConfig):
        self.config = config
        self.apple = Apple(config.element_size, config.grid_size_x, config.grid_size_y,
                           config.game_board_loc_x, config.game_board_loc_y)
        self.snake = Snake(config.element_size, config.game_board_loc_x, config.game_board_loc_y, config.grid_size_x, config.grid_size_y)
        self.running = True

        self.hit_sound = pygame.mixer.Sound('media/snake/hit.wav')
        self.hit_sound.set_volume(0.40)
        self.eat_sound = pygame.mixer.Sound('media/snake/eat.wav')
        self.eat_sound.set_volume(0.40)

        self.menu = InGameMenu(screen, 139, 180,
                               config.primary_color,
                               config.secondary_color,
                               config.highlight_color,
                               config.hover_color)

        self.grid_size_x = config.grid_size_x
        self.grid_size_y = config.grid_size_y

        self.score = 0

    def update_logic(self):
        if self.running:
            self.try_eating_apple()
            self.check_self_collision()
            self.check_border_collision()
            if self.running:
                try:
                    self.snake.move()
                except Exception as e:
                    if str(e) in ["self_collision", "border_collision"]:
                        self.fail()

    def draw_objects(self, screen):
        self.apple.draw(screen)
        self.snake.draw(screen)
        self.draw_score(screen)

    def try_eating_apple(self):
        if self.apple.position == self.snake.body[0]:
            self.snake.grow = True
            self.score += 1
            self.eat_sound.play()
            self.apple.reposition(self.snake)

        if len(self.snake.body) - 3 >= 245:
            self.running = False
            self.menu.enable_menu(MenuType.WIN)

    def check_self_collision(self):
        direction = self.snake.direction_queue[0] if self.snake.direction_queue else self.snake.direction
        upcoming_position = self.snake.body[0] + direction

        for coordinates in self.snake.body[:-1]: #Not counting the tail to avoid unnecessary crashes
            if upcoming_position == coordinates:
                self.fail()

    def check_border_collision(self):
        direction = self.snake.direction_queue[0] if self.snake.direction_queue else self.snake.direction
        upcoming_position = self.snake.body[0] + direction

        if (
            upcoming_position.x < 0 or
            upcoming_position.x >= self.grid_size_x or
            upcoming_position.y < 0 or
            upcoming_position.y >= self.grid_size_y
        ):
            self.fail()

    def fail(self):
        self.running = False
        self.hit_sound.play()
        self.menu.enable_menu(MenuType.LOSS)

    def draw_score(self, screen):
        score_border = pygame.Rect(314, 14, 169, 84)
        font = pygame.font.Font('media/snake/Jersey25-Regular.ttf', 95)
        score_surface = font.render(str(self.score), True, '#d3e671')
        score_rectangle = score_surface.get_rect(center=score_border.center)

        pygame.draw.rect(screen, "#4d6127", score_border)
        screen.blit(score_surface, score_rectangle)

    def get_game_speed(self):
        score = len(self.snake.body) - 3
        return max(120, 200 - (score * 5))