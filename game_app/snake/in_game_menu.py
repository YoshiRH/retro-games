import pygame
from enum import Enum

class InGameMenu:
    def __init__(self, screen, pos_left, pos_top, primary_color, secondary_color, highlight_color, hover_color):
        self.screen = screen
        self.active = False
        sizes = {"big": 75, "medium": 55, "small": 30}
        self.fonts = {k: pygame.font.Font('media/snake/Jersey25-Regular.ttf', v) for k, v in sizes.items()}
        self.pos_left = pos_left
        self.pos_top = pos_top
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.highlight_color = highlight_color
        self.hover_color = hover_color
        self.left_button_rect = pygame.Rect(self.pos_left + 41, self.pos_top + 220, 200, 60)
        self.right_button_rect= pygame.Rect(self.pos_left + 281, self.pos_top + 220, 200, 60)
        self.type = MenuType.NONE

    def disable(self):
        self.active = False

    def draw_current(self, score):
        if not self.active:
            return

        if self.type is MenuType.START:
            self.draw_base("Collect Apples", "Use WASD keys to switch direction", "", "Start", "Leave")
        elif self.type is MenuType.PAUSE:
            self.draw_base("Game paused", "", "", "Continue", "Leave")
        elif self.type is MenuType.WIN:
            self.draw_base("You won!", f"All apples collected :)", "", "Retry", "Leave")
        elif self.type is MenuType.LOSS:
            self.draw_base("You lost!", f"Final Score: {score}", "", "Retry", "Leave")

    def enable_menu(self, menu_type):
        self.type = menu_type
        self.active = True

    def draw_base(self, title, additional, row_2, left, right):
        mouse_pos = pygame.mouse.get_pos()

        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((50, 50, 50, 180))
        self.screen.blit(overlay, (0, 0))

        border = pygame.Rect(self.pos_left, self.pos_top, 525, 350)
        pygame.draw.rect(self.screen, self.secondary_color, border)

        inside = pygame.Rect(self.pos_left + 30, self.pos_top + 30, 465, 290)
        pygame.draw.rect(self.screen, self.primary_color, inside)

        title = self.fonts["big"].render(title, True, self.secondary_color)
        title_rect = title.get_rect(center=(self.pos_left + 525 // 2, self.pos_top + 70))
        self.screen.blit(title, title_rect)

        additional = self.fonts["small"].render(additional, True, self.secondary_color)
        score_rect = additional.get_rect(center=(self.pos_left + 525 // 2, self.pos_top + 140))
        self.screen.blit(additional, score_rect)

        row_2_surface = self.fonts["small"].render(row_2, True, self.secondary_color)
        score_rect = row_2_surface.get_rect(center=(self.pos_left + 525 // 2, self.pos_top + 175))
        self.screen.blit(row_2_surface, score_rect)

        # Left button
        left_hovered = self.left_button_rect.collidepoint(mouse_pos)
        left_color = self.hover_color if left_hovered else (77, 97, 39)
        pygame.draw.rect(self.screen, left_color, self.left_button_rect)

        left_text = self.fonts["medium"].render(left, True, (211, 230, 113))
        left_text_rect = left_text.get_rect(center=self.left_button_rect.center)
        self.screen.blit(left_text, left_text_rect)

        # Right button
        right_hovered = self.right_button_rect.collidepoint(mouse_pos)
        right_color = self.hover_color if right_hovered else (77, 97, 39)
        pygame.draw.rect(self.screen, right_color, self.right_button_rect)

        right_text = self.fonts["medium"].render(right, True, (211, 230, 113))
        right_text_rect = right_text.get_rect(center=self.right_button_rect.center)
        self.screen.blit(right_text, right_text_rect)

    def handle_event(self, event):
        if self.active and event.type == pygame.MOUSEBUTTONDOWN:
            if self.type in [MenuType.PAUSE, MenuType.LOSS, MenuType.WIN, MenuType.START]:
                if self.left_button_rect.collidepoint(event.pos):
                    return {
                        MenuType.PAUSE: "continue",
                        MenuType.LOSS: "retry",
                        MenuType.WIN: "retry",
                        MenuType.START: "start"
                    }.get(self.type)
                if self.right_button_rect.collidepoint(event.pos):
                    return "quit"
        return None

class MenuType(Enum):
    NONE = 0
    START = 1
    PAUSE = 2
    WIN = 3
    LOSS = 4