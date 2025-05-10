import pygame
import os
from pygame.math import Vector2
import random

# Game board dimensions
game_board_element_size = 35
game_board_grid_size_x = 21
game_board_grid_size_y = 12
game_board_x = 34
game_board_y = 145
paddle_width = 15
paddle_height = 70
ball_size = 10

class Paddle:
    def __init__(self, x, is_player):
        self.position = Vector2(x, game_board_y + (game_board_grid_size_y * game_board_element_size) / 2)
        self.height = paddle_height
        self.width = paddle_width
        self.speed = 5
        self.is_player = is_player
        self.sprite = pygame.Surface((self.width, self.height))
        self.sprite.fill("#2AEBAF")

    def move(self, direction, screen_height):
        self.position.y += direction * self.speed
        if self.position.y < game_board_y:
            self.position.y = game_board_y
        if self.position.y + self.height > game_board_y + game_board_grid_size_y * game_board_element_size:
            self.position.y = game_board_y + game_board_grid_size_y * game_board_element_size - self.height

    def ai_move(self, ball, screen_height):
        if ball.position.y > self.position.y + self.height / 2:
            self.move(1, screen_height)
        elif ball.position.y < self.position.y + self.height / 2:
            self.move(-1, screen_height)

    def draw(self, screen):
        rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        screen.blit(self.sprite, rect)

class Ball:
    def __init__(self):
        self.position = Vector2(game_board_x + (game_board_grid_size_x * game_board_element_size) / 2,
                                game_board_y + (game_board_grid_size_y * game_board_element_size) / 2)
        self.speed = Vector2(random.choice([-5, 5]), random.uniform(-3, 3))
        self.size = ball_size
        self.sprite = pygame.Surface((self.size, self.size))
        self.sprite.fill("#2AEBAF")

    def move(self):
        self.position += self.speed

    def draw(self, screen):
        rect = pygame.Rect(self.position.x - self.size / 2, self.position.y - self.size / 2, self.size, self.size)
        screen.blit(self.sprite, rect)

    def reset(self):
        self.position = Vector2(game_board_x + (game_board_grid_size_x * game_board_element_size) / 2,
                                game_board_y + (game_board_grid_size_y * game_board_element_size) / 2)
        self.speed = Vector2(random.choice([-5, 5]), random.uniform(-3, 3))

class Game:
    def __init__(self):
        self.player = Paddle(game_board_x + 20, True)
        self.opponent = Paddle(game_board_x + (game_board_grid_size_x * game_board_element_size) - 20 - paddle_width, False)
        self.ball = Ball()
        self.player_score = 0
        self.opponent_score = 0
        self.running = True
        self.game_started = False
        self.max_score = 5
        self.key_states = {'w': False, 's': False}
        self.end_pop_up = pygame.image.load('media/snake/endPopUp.png').convert_alpha()

    def update_logic(self):
        if self.running and self.game_started:
            self.ball.move()
            self.opponent.ai_move(self.ball, 600)
            self.check_collisions()
            self.check_score()
        if self.key_states['w']:
            self.player.move(-1, 600)
        if self.key_states['s']:
            self.player.move(1, 600)

    def draw_objects(self, screen):
        self.player.draw(screen)
        self.opponent.draw(screen)
        self.ball.draw(screen)
        self.draw_score(screen)
        if not self.game_started:
            self.draw_start_screen(screen)
        if not self.running:
            self.draw_end_screen(screen)

    def check_collisions(self):
        if self.ball.position.y - self.ball.size / 2 <= game_board_y or \
           self.ball.position.y + self.ball.size / 2 >= game_board_y + game_board_grid_size_y * game_board_element_size:
            self.ball.speed.y = -self.ball.speed.y

        ball_rect = pygame.Rect(self.ball.position.x - self.ball.size / 2, self.ball.position.y - self.ball.size / 2,
                                self.ball.size, self.ball.size)
        player_rect = pygame.Rect(self.player.position.x, self.player.position.y,
                                  self.player.width, self.player.height)
        opponent_rect = pygame.Rect(self.opponent.position.x, self.opponent.position.y,
                                    self.opponent.width, self.opponent.height)

        if ball_rect.colliderect(player_rect) or ball_rect.colliderect(opponent_rect):
            self.ball.speed.x = -self.ball.speed.x
            self.ball.speed *= 1.05

    def check_score(self):
        if self.ball.position.x - self.ball.size / 2 <= game_board_x:
            self.opponent_score += 1
            self.ball.reset()
            if self.opponent_score >= self.max_score:
                self.running = False
        elif self.ball.position.x + self.ball.size / 2 >= game_board_x + game_board_grid_size_x * game_board_element_size:
            self.player_score += 1
            self.ball.reset()
            if self.player_score >= self.max_score:
                self.running = False

    def draw_score(self, screen):
        font = pygame.font.Font('media/snake/VT323-Regular.ttf', 110)
        score_border = pygame.Rect(314, 14, 169, 84)
        pygame.draw.rect(screen, "#1E1E1E", score_border)
        player_score_surface = font.render(str(self.player_score), True, '#2AEBAF')
        screen.blit(player_score_surface, (330, 0))
        opponent_score_surface = font.render(str(self.opponent_score), True, '#2AEBAF')
        screen.blit(opponent_score_surface, (430, 0))

    def draw_start_screen(self, screen):
        font = pygame.font.Font('media/snake/VT323-Regular.ttf', 40)
        text = font.render("Press Enter to Start", True, '#2AEBAF')
        text_rect = text.get_rect(center=(400, 300))
        screen.blit(text, text_rect)

    def draw_end_screen(self, screen):
        rectangle = pygame.Rect(139, 180, 525, 350)
        screen.blit(self.end_pop_up, rectangle)

def draw_game_board(screen):
    screen.fill("#1E1E1E")
    dash_height = 20
    gap_height = 20
    line_x = game_board_x + (game_board_grid_size_x * game_board_element_size) // 2 - 2
    for y in range(game_board_y, game_board_y + game_board_grid_size_y * game_board_element_size, dash_height + gap_height):
        dash_rect = pygame.Rect(line_x, y, 4, dash_height)
        pygame.draw.rect(screen, "#2AEBAF", dash_rect)

def main(root=None):
    pygame.init()
    if root:
        os.environ['SDL_WINDOWID'] = str(root.winfo_id())
        pygame.display.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    game = Game()

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 16)  # ~60 FPS

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    game = Game()
                elif event.key == pygame.K_w:
                    game.key_states['w'] = True
                elif event.key == pygame.K_s:
                    game.key_states['s'] = True
                elif event.key == pygame.K_RETURN and not game.game_started:
                    game.game_started = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    game.key_states['w'] = False
                elif event.key == pygame.K_s:
                    game.key_states['s'] = False
            if event.type == SCREEN_UPDATE:
                game.update_logic()

        draw_game_board(screen)
        game.draw_objects(screen)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
