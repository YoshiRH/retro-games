import pygame

class InGameMenu:
    def __init__(self, screen):
        self.screen = screen
        self.active = False
        self.font = pygame.font.SysFont(None, 60)
        self.quit_button_rect = pygame.Rect(300, 350, 200, 60)

    def toggle(self):
        self.active = not self.active

    def draw(self):
        if self.active:
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            title = self.font.render("Pause", True, (255, 255, 255))
            title_rect = title.get_rect(center=(400, 200))
            self.screen.blit(title, title_rect)

            pygame.draw.rect(self.screen, (150, 0, 0), self.quit_button_rect)
            quit_text = self.font.render("Leave", True, (255, 255, 255))
            quit_text_rect = quit_text.get_rect(center=self.quit_button_rect.center)
            self.screen.blit(quit_text, quit_text_rect)

    def handle_event(self, event):
        if self.active and event.type == pygame.MOUSEBUTTONDOWN:
            if self.quit_button_rect.collidepoint(event.pos):
                return "quit"
        return None