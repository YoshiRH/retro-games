import pygame, os
from pygame.math import Vector2
from .in_game_menu import MenuType
from .additional import draw_game_board
from .game import Game
from .game_config import GameConfig

def main(root):
    # Initialization
    pygame.mixer.pre_init(44100, -16, 2, 64)
    pygame.mixer.init()
    pygame.init()

    os.environ['SDL_WINDOWID'] = str(root.winfo_id())
    pygame.display.init()

    screen = pygame.display.set_mode((800,600))
    clock = pygame.time.Clock()

    config = GameConfig()
    game = Game(screen, config)

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 120)

    game.menu.enable_menu(MenuType.START)

    #Main game loop
    running = True
    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                continue

            # Menu
            if game.menu.active:
                result = game.menu.handle_event(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if game.menu.type == MenuType.PAUSE:
                        game.menu.disable_menu()
                elif result == "quit":
                    running = False
                elif result == "continue" or result == "start":
                    game.menu.disable_menu()
                elif result == "retry":
                    game = Game(screen, config)
                continue

            # Game Input
            if event.type == pygame.KEYDOWN:
                game = handle_game_input(event.key, game, config, screen)

            # Logic update
            if event.type == SCREEN_UPDATE:
                pygame.time.set_timer(SCREEN_UPDATE, game.get_game_speed())
                game.update_logic()

        # Drawing
        screen.fill("#89ac46")
        draw_game_board(screen, config)
        game.draw_objects(screen)
        game.menu.draw_current(game.score, game.best_score)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

def handle_game_input(key, game, config, screen):
    match key:
        case pygame.K_ESCAPE:
            game.menu.enable_menu(MenuType.PAUSE)
        case pygame.K_r:
            return Game(screen, config)
        case pygame.K_w:
            game.snake.queue_direction(Vector2(0, -1))
        case pygame.K_s:
            game.snake.queue_direction(Vector2(0, 1))
        case pygame.K_a:
            game.snake.queue_direction(Vector2(-1, 0))
        case pygame.K_d:
            game.snake.queue_direction(Vector2(1, 0))
    return game

if __name__ == "__main__":
    main()