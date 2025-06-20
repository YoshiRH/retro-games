import pygame, os
from .snake import Apple, Snake
from .in_game_menu import InGameMenu, MenuType
from .game_config import GameConfig

class Game:
    """
    Main game controller class for the Snake game.

    Manages core gameplay logic, such as movement, collision detection, scoring,
    sound effects, and game state transitions (e.g., win, loss, pause).

    Parameters
    ----------
    screen : pygame.Surface
        The surface on which the game elements are drawn.
    config : GameConfig
        The configuration object containing gameplay and UI settings.
    """

    def __init__(self, screen, config: GameConfig):
        self.apple = Apple(config.element_size, config.grid_size_x, config.grid_size_y,
                           config.game_board_loc_x, config.game_board_loc_y)
        self.snake = Snake(config.element_size, config.game_board_loc_x, config.game_board_loc_y,
                           config.grid_size_x, config.grid_size_y)
        self.menu = InGameMenu(screen, 139, 180,
                               config.primary_color, config.secondary_color,
                               config.highlight_color, config.hover_color)

        self.score = 0
        self.best_score = self._load_best_score()

        self._config = config
        self._hit_sound = pygame.mixer.Sound('media/snake/hit.wav')
        self._hit_sound.set_volume(0.40)
        self._eat_sound = pygame.mixer.Sound('media/snake/eat.wav')
        self._eat_sound.set_volume(0.40)
        self._font = pygame.font.Font('media/snake/Jersey25-Regular.ttf', 95)
        self._running = True

    def update_logic(self):
        """
        Updates the game logic for a single frame.

        Handles apple consumption, collisions (self or border),
        and snake movement if the game is still running.
        """
        if self._running:
            self._try_eating_apple()
            self._check_self_collision()
            self._check_border_collision()
            if self._running:
                self.snake.move()

    def draw_objects(self, screen):
        """
        Draws all game elements onto the screen: the snake, the apple,
        and the current score.

        Parameters
        ----------
        screen : pygame.Surface
            The surface to draw the game elements on.
        """
        self.apple.draw(screen)
        self.snake.draw(screen)
        self._draw_score(screen)

    def get_game_speed(self):
        """
        Calculates the current game speed based on the snake's length.

        Returns
        -------
        int
            The time delay (in milliseconds) between snake moves. Capped at 120 ms.
        """
        score = len(self.snake.body) - 3
        return max(120, 200 - (score * 5))

    def _draw_score(self, screen):
        """
        Renders the current score on the screen.

        Parameters
        ----------
        screen : pygame.Surface
            The surface to render the score on.
        """
        score_border = pygame.Rect(self._config.score_display_loc_x, self._config.score_display_loc_y, 169, 84)
        score_surface = self._font.render(str(self.score), True, '#d3e671')
        score_rectangle = score_surface.get_rect(center=score_border.center)

        pygame.draw.rect(screen, "#4d6127", score_border)
        screen.blit(score_surface, score_rectangle)

    def _fail(self):
        """
        Triggers the loss condition for the game.

        Stops gameplay, plays the fail sound, updates the best score if needed,
        and displays the appropriate end-game menu.
        """
        self._running = False
        self.snake.alive = False
        self._hit_sound.play()

        if self.score > self.best_score:
            self.best_score = self.score
            self._save_best_score()
            self.menu.enable_menu(MenuType.NEW_RECORD)
        else:
            self.menu.enable_menu(MenuType.LOSS)

    def _try_eating_apple(self):
        """
        Checks if the snake's head is at the apple's position.

        If so, increases the score, grows the snake, plays the sound,
        and repositions the apple. Triggers win state if the board is filled.
        """
        if self.apple.position == self.snake.body[0]:
            self.snake.grow = True
            self.score += 1
            self._eat_sound.play()

            if self.score >= (self._config.grid_size_x * self._config.grid_size_y - 5):
                self._running = False
                self.menu.enable_menu(MenuType.WIN)
            self.apple.reposition(self.snake)

    def _check_self_collision(self):
        """
        Checks whether the snake will collide with its own body
        on the next move. Triggers `fail()` if a collision is detected.
        """
        direction = self.snake.direction_queue[0] if self.snake.direction_queue else self.snake.direction
        upcoming_position = self.snake.body[0] + direction

        # If snake will grow, the tail won't be removed, so include it in the check
        check_body = self.snake.body[1:] if self.snake.grow else self.snake.body[1:-1]
        if upcoming_position in check_body:
            self._fail()

    def _check_border_collision(self):
        """
        Checks whether the snake's next move will result in
        a collision with the game board boundary. Triggers `fail()` if true.
        """
        direction = self.snake.direction_queue[0] if self.snake.direction_queue else self.snake.direction
        upcoming_position = self.snake.body[0] + direction

        if (upcoming_position.x < 0 or upcoming_position.x >= self._config.grid_size_x or
            upcoming_position.y < 0 or upcoming_position.y >= self._config.grid_size_y):
            self._fail()

    @staticmethod
    def _load_best_score():
        """
        Loads the best score from a local file.

        Returns
        -------
        int
            The best score stored, or 0 if the file doesn't exist or is invalid.
        """
        if os.path.exists("snake/best_score.txt"):
            try:
                with open("snake/best_score.txt", "r") as f:
                    return int(f.read())
            except ValueError:
                return 0
        return 0

    def _save_best_score(self):
        """
        Saves the current best score to a file.
        Creates the directory if it doesn't exist.
        """
        os.makedirs("snake", exist_ok=True)
        with open("snake/best_score.txt", "w") as f:
            f.write(str(self.best_score))