import pygame
from .game_config import GameConfig

def draw_game_board(screen, config: GameConfig):
    game_board_border = pygame.Rect(0, 112, 800, 488)
    game_board = pygame.Rect(config.game_board_loc_x, config.game_board_loc_y,
                             config.grid_size_x * config.element_size,
                             config.grid_size_y * config.element_size)

    pygame.draw.rect(screen, config.secondary_color, game_board_border)
    pygame.draw.rect(screen, config.highlight_color, game_board)

    for y in range(config.grid_size_y):
        for x in range(config.grid_size_x):
            if (y % 2 == 0 and x % 2 == 0) or (y % 2 == 1 and x % 2 == 1):
                rect = pygame.Rect(
                    config.game_board_loc_x + (x * config.element_size),
                    config.game_board_loc_y + (y * config.element_size),
                    config.element_size,
                    config.element_size
                )
                pygame.draw.rect(screen, config.primary_color, rect)