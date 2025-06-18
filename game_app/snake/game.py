import pygame, os
from .snake import Apple, Snake
from .in_game_menu import InGameMenu, MenuType
from .game_config import GameConfig

class Game:
    def __init__(self, screen, config: GameConfig):
        self.config = config
        self.apple = Apple(config.element_size, config.grid_size_x, config.grid_size_y,
                           config.game_board_loc_x, config.game_board_loc_y)
        self.snake = Snake(config.element_size, config.game_board_loc_x, config.game_board_loc_y,
                           config.grid_size_x, config.grid_size_y)
        self.menu = InGameMenu(screen, 139, 180,
                               config.primary_color, config.secondary_color,
                               config.highlight_color, config.hover_color)

        self.hit_sound = pygame.mixer.Sound('media/snake/hit.wav')
        self.hit_sound.set_volume(0.40)
        self.eat_sound = pygame.mixer.Sound('media/snake/eat.wav')
        self.eat_sound.set_volume(0.40)
        self.font = pygame.font.Font('media/snake/Jersey25-Regular.ttf', 95)

        self.running = True
        self.score = 0
        self.best_score = self.load_best_score()

    def update_logic(self):
        if self.running:
            self.try_eating_apple()
            self.check_self_collision()
            self.check_border_collision()
            if self.running:
                self.snake.move()

    def draw_objects(self, screen):
        self.apple.draw(screen)
        self.snake.draw(screen)
        self.draw_score(screen)

    def try_eating_apple(self):
        if self.apple.position == self.snake.body[0]:
            self.snake.grow = True
            self.score += 1
            self.eat_sound.play()

            if self.score >= (self.config.grid_size_x * self.config.grid_size_y - 5):
                self.running = False
                self.menu.enable_menu(MenuType.WIN)
            self.apple.reposition(self.snake)

    def check_self_collision(self):
        direction = self.snake.direction_queue[0] if self.snake.direction_queue else self.snake.direction
        upcoming_position = self.snake.body[0] + direction

        # If snake will grow, the tail won't be removed, so include it in the check
        check_body = self.snake.body[1:] if self.snake.grow else self.snake.body[1:-1]
        if upcoming_position in check_body:
            self.fail()

    def check_border_collision(self):
        direction = self.snake.direction_queue[0] if self.snake.direction_queue else self.snake.direction
        upcoming_position = self.snake.body[0] + direction

        if (upcoming_position.x < 0 or upcoming_position.x >= self.config.grid_size_x or
            upcoming_position.y < 0 or upcoming_position.y >= self.config.grid_size_y):
            self.fail()

    def fail(self):
        self.running = False
        self.snake.alive = False
        self.hit_sound.play()

        if self.score > self.best_score:
            self.best_score = self.score
            self.save_best_score()
            self.menu.enable_menu(MenuType.NEW_RECORD)
        else:
            self.menu.enable_menu(MenuType.LOSS)

    def draw_score(self, screen):
        score_border = pygame.Rect(self.config.score_display_loc_x, self.config.score_display_loc_y, 169, 84)
        score_surface = self.font.render(str(self.score), True, '#d3e671')
        score_rectangle = score_surface.get_rect(center=score_border.center)

        pygame.draw.rect(screen, "#4d6127", score_border)
        screen.blit(score_surface, score_rectangle)

    def get_game_speed(self):
        """
        Returns the delay in milliseconds between moves.
        Snake starts slow (200 ms) and gets faster as it grows.
        Speed caps at 120 ms.
        """
        score = len(self.snake.body) - 3
        return max(120, 200 - (score * 5))

    @staticmethod
    def load_best_score():
        if os.path.exists("snake/best_score.txt"):
            try:
                with open("snake/best_score.txt", "r") as f:
                    return int(f.read())
            except ValueError:
                return 0
        return 0

    def save_best_score(self):
        os.makedirs("snake", exist_ok=True)
        with open("snake/best_score.txt", "w") as f:
            f.write(str(self.best_score))