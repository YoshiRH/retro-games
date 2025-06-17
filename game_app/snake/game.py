import pygame
from .snake import Apple, Snake
from .in_game_menu import InGameMenu, MenuType

class Game:
    def __init__(
        self,
        screen,
        element_size,
        grid_size_x,
        grid_size_y,
        game_board_loc_x,
        game_board_loc_y,
        primary_color,
        secondary_color,
        highlight_color,
        hover_color
    ):
        self.element_size = element_size
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y
        self.game_board_loc_x = game_board_loc_x
        self.game_board_loc_y = game_board_loc_y

        self.apple = Apple(element_size, grid_size_x, grid_size_y, game_board_loc_x, game_board_loc_y)
        self.snake = Snake(element_size, game_board_loc_x, game_board_loc_y)
        self.running = True

        self.hit_sound = pygame.mixer.Sound('media/snake/hit.wav')
        self.hit_sound.set_volume(0.40)

        self.eat_sound = pygame.mixer.Sound('media/snake/eat.wav')
        self.eat_sound.set_volume(0.40)

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
        score = str(len(self.snake.body) - 3)
        score_surface = font.render(score, True, '#d3e671')
        score_rectangle = score_surface.get_rect(center=score_border.center)

        pygame.draw.rect(screen, "#4d6127", score_border)
        screen.blit(score_surface, score_rectangle)

    def get_game_speed(self):
        score = len(self.snake.body) - 3
        return max(120, 200 - (score * 5))