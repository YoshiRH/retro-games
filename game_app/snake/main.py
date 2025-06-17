import pygame, os
from pygame.math import Vector2
from .in_game_menu import MenuType
from .additional import draw_game_board
from .game import Game
from .game_config import GameConfig

def main(root):
    # Initialization and embed inside the Tkinter Window
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
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        if not game.menu.active:
                            game.menu.enable_menu(MenuType.PAUSE)
                        else:
                            game.menu.active = False
                    case pygame.K_r:
                        game = Game(screen, config)
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
                    game = Game(screen, config)
                elif result == "start":
                    game.menu.disable()
            if event.type == SCREEN_UPDATE and not game.menu.active:
                pygame.time.set_timer(SCREEN_UPDATE, game.get_game_speed())
                game.update_logic()
        screen.fill("#89ac46")
        draw_game_board(screen, config)
        game.draw_objects(screen)

        game.menu.draw_current(len(game.snake.body) - 3)

        pygame.display.update()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()