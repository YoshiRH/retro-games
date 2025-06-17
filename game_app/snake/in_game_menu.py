import pygame

class InGameMenu:
    def __init__(self, screen, pos_left, post_top, primary_color, secondary_color, highlight_color):
        self.screen = screen
        self.active = False
        self.font = pygame.font.SysFont(None, 60)
        self.big_font = pygame.font.Font('media/snake/VT323-Regular.ttf', 80)
        self.medium_font = pygame.font.Font('media/snake/VT323-Regular.ttf', 60)
        self.small_font = pygame.font.Font('media/snake/VT323-Regular.ttf', 40)
        self.pos_left = pos_left
        self.pos_top = post_top
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.highlight_color = highlight_color
        self.left_button_rect = pygame.Rect(self.pos_left + 41, self.pos_top + 220, 200, 60)
        self.right_button_rect= pygame.Rect(self.pos_left + 281, self.pos_top + 220, 200, 60)
        self.type = "none"

    def disable(self):
        self.active = False

    def draw_current(self, score):
        if not self.active:
            return

        if self.type == "start":
            self.draw_base("Collect Apples", "Use Arrow/WASD keys to steer", "Start", "Leave")
        elif self.type == "pause":
            self.draw_base("Game paused", "", "Continue", "Leave")
        elif self.type == "win":
            self.draw_base("You won!", f"All apples collected :)", "Retry", "Leave")
        elif self.type == "loss":
            self.draw_base("You lost!", f"Final Score: {score}", "Retry", "Leave")

    def enable_menu(self, type):
        self.type = type
        # todo input check
        self.active = True

    def draw_base(self, title, additional, left, right):
        if self.active:
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((50, 50, 50, 180))
            self.screen.blit(overlay, (0, 0))

            border = pygame.Rect(self.pos_left, self.pos_top, 525, 350)
            pygame.draw.rect(self.screen, self.secondary_color, border)

            inside = pygame.Rect(self.pos_left + 30, self.pos_top + 30, 465, 290)
            pygame.draw.rect(self.screen, self.primary_color, inside)

            title = self.big_font.render(title, True, (77, 97, 39))
            title_rect = title.get_rect(center=(self.pos_left + 525 // 2, self.pos_top + 70))
            self.screen.blit(title, title_rect)

            additional = self.small_font.render(additional, True, (77, 97, 39))
            score_rect = additional.get_rect(center=(self.pos_left + 525 // 2, self.pos_top + 140))
            self.screen.blit(additional, score_rect)

            pygame.draw.rect(self.screen, (77, 97, 39), self.left_button_rect)
            left_text = self.medium_font.render(left, True, (211, 230, 113))
            left_text_rect = left_text.get_rect(center=self.left_button_rect.center)
            self.screen.blit(left_text, left_text_rect)

            pygame.draw.rect(self.screen, (77, 97, 39), self.right_button_rect)
            right_text = self.medium_font.render(right, True, (211, 230, 113))
            right_text_rect = right_text.get_rect(center=self.right_button_rect.center)
            self.screen.blit(right_text, right_text_rect)

    def handle_event(self, event):
        if self.active and event.type == pygame.MOUSEBUTTONDOWN:
            if self.type in ["pause", "loss", "win", "start"]:
                if self.left_button_rect.collidepoint(event.pos):
                    return {
                        "pause": "continue",
                        "loss": "retry",
                        "win": "retry",
                        "start": "start"
                    }[self.type]
                if self.right_button_rect.collidepoint(event.pos):
                    return "quit" if self.type == "pause" else "exit"
        return None