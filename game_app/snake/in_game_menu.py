import pygame
from enum import Enum

class InGameMenu:
    def __init__(self, screen, pos_left, pos_top, primary_color, secondary_color, highlight_color, hover_color):
        self.type = MenuType.NONE
        self.active = False

        self._screen = screen
        sizes = {"big": 75, "medium": 55, "small": 30}
        self._fonts = {k: pygame.font.Font('media/snake/Jersey25-Regular.ttf', v) for k, v in sizes.items()}

        self._pos_left = pos_left
        self._pos_top = pos_top
        self._left_button_rect = pygame.Rect(self._pos_left + 41, self._pos_top + 220, 200, 60)
        self._right_button_rect = pygame.Rect(self._pos_left + 281, self._pos_top + 220, 200, 60)

        self._primary_color = primary_color
        self._secondary_color = secondary_color
        self._highlight_color = highlight_color
        self._hover_color = hover_color

    def disable_menu(self):
        self.active = False

    def draw_current(self, current_score, best_score):
        if not self.active:
            return

        if self.type is MenuType.START:
            row_2 = f"Best Score: {best_score}" if best_score > 0 else ""
            self._draw_base("Collect Apples", "Use WASD keys to switch direction", row_2, "Start", "Leave")
        elif self.type is MenuType.PAUSE:
            self._draw_base("Game paused", "", "", "Continue", "Leave")
        elif self.type is MenuType.WIN:
            self._draw_base("You won!", f"All apples collected :)", "", "Retry", "Leave")
        elif self.type is MenuType.LOSS:
            self._draw_base("You lost!", f"Final Score: {current_score}", f"Best Score: {best_score}", "Retry", "Leave")
        elif self.type is MenuType.NEW_RECORD:
            self._draw_base("New record!", f"Congratulations on getting a record!", f"The new best score is {current_score}", "Retry", "Leave")

    def enable_menu(self, menu_type):
        self.type = menu_type
        self.active = True

    def handle_event(self, event):
        if self.active and event.type == pygame.MOUSEBUTTONDOWN:
            if self.type in [MenuType.PAUSE, MenuType.LOSS, MenuType.WIN, MenuType.START, MenuType.NEW_RECORD]:
                if self._left_button_rect.collidepoint(event.pos):
                    return {
                        MenuType.PAUSE: "continue",
                        MenuType.LOSS: "retry",
                        MenuType.WIN: "retry",
                        MenuType.START: "start",
                        MenuType.NEW_RECORD: "retry"
                    }[self.type]
                if self._right_button_rect.collidepoint(event.pos):
                    return "quit"
        return None

    def _draw_base(self, title, info_1, info_2, left, right):
        mouse_pos = pygame.mouse.get_pos()

        overlay = pygame.Surface(self._screen.get_size(), pygame.SRCALPHA)
        overlay.fill((50, 50, 50, 180))
        self._screen.blit(overlay, (0, 0))

        border = pygame.Rect(self._pos_left, self._pos_top, 525, 350)
        pygame.draw.rect(self._screen, self._secondary_color, border)

        inside = pygame.Rect(self._pos_left + 30, self._pos_top + 30, 465, 290)
        pygame.draw.rect(self._screen, self._primary_color, inside)

        title = self._fonts["big"].render(title, True, self._secondary_color)
        title_rect = title.get_rect(center=(self._pos_left + 525 // 2, self._pos_top + 70))
        self._screen.blit(title, title_rect)

        info_1 = self._fonts["small"].render(info_1, True, self._secondary_color)
        info_rect = info_1.get_rect(center=(self._pos_left + 525 // 2, self._pos_top + 140))
        self._screen.blit(info_1, info_rect)

        info_2 = self._fonts["small"].render(info_2, True, self._secondary_color)
        info_rect = info_2.get_rect(center=(self._pos_left + 525 // 2, self._pos_top + 175))
        self._screen.blit(info_2, info_rect)

        # Left button
        left_hovered = self._left_button_rect.collidepoint(mouse_pos)
        left_color = self._hover_color if left_hovered else (77, 97, 39)
        pygame.draw.rect(self._screen, left_color, self._left_button_rect)

        left_text = self._fonts["medium"].render(left, True, (211, 230, 113))
        left_text_rect = left_text.get_rect(center=self._left_button_rect.center)
        self._screen.blit(left_text, left_text_rect)

        # Right button
        right_hovered = self._right_button_rect.collidepoint(mouse_pos)
        right_color = self._hover_color if right_hovered else (77, 97, 39)
        pygame.draw.rect(self._screen, right_color, self._right_button_rect)

        right_text = self._fonts["medium"].render(right, True, (211, 230, 113))
        right_text_rect = right_text.get_rect(center=self._right_button_rect.center)
        self._screen.blit(right_text, right_text_rect)

class MenuType(Enum):
    NONE = 0
    START = 1
    PAUSE = 2
    WIN = 3
    LOSS = 4
    NEW_RECORD = 5