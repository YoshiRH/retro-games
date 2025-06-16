import pygame

class InGameMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 60)
        self.active = False

    def toggle(self):
        self.active = not self.active

    def draw(self):
        if self.active:
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            text = self.font.render("Pause", True, (255, 255, 255))
            rect = text.get_rect(center=self.screen.get_rect().center)
            self.screen.blit(text, rect)