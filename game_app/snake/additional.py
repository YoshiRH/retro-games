import pygame

def draw_game_board(screen, element_size, grid_size_x, grid_size_y, loc_x, loc_y, primary_color, secondary_color, highlight_color):
    game_board_border = pygame.Rect(0, 112, 800, 488)
    game_board = pygame.Rect(loc_x, loc_y,
                             (grid_size_x * element_size),
                             (grid_size_y * element_size))
    pygame.draw.rect(screen, secondary_color, game_board_border)
    pygame.draw.rect(screen, highlight_color, game_board)
    for y in range (grid_size_y):
        for x in range(grid_size_x):
            if y % 2 == 0:
                if x % 2 == 0:
                    rectangle = pygame.Rect(loc_x + (x * element_size),
                                            loc_y + (y * element_size)
                                            , element_size, element_size)
                    pygame.draw.rect(screen, primary_color, rectangle)
            else:
                if x % 2 == 1:
                    rectangle = pygame.Rect(loc_x + (x * element_size),
                                            loc_y + (y * element_size)
                                            , element_size, element_size)
                    pygame.draw.rect(screen, primary_color, rectangle)