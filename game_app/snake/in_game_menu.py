import pygame

class InGameMenu:
    def __init__(self, screen):
        self.screen = screen
        self.active = False
        self.font = pygame.font.SysFont(None, 60)
        self.big_font = pygame.font.Font('media/snake/VT323-Regular.ttf', 80)
        self.medium_font = pygame.font.Font('media/snake/VT323-Regular.ttf', 60)
        self.small_font = pygame.font.Font('media/snake/VT323-Regular.ttf', 40)
        self.continue_button_rect = pygame.Rect(180, 400, 200, 60)
        self.quit_button_rect = pygame.Rect(420, 400, 200, 60)

    def toggle(self):
        self.active = not self.active

    def draw(self):
        if self.active:
            #background
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((50, 50, 50, 180))
            self.screen.blit(overlay, (0, 0))

            #base
            menu_border = pygame.Rect(139, 180, 525, 350)
            pygame.draw.rect(self.screen, "#4d6127", menu_border)

            menu_inside = pygame.Rect(169, 210, 465, 290)
            pygame.draw.rect(self.screen, "#89ac46", menu_inside)


            title = self.big_font.render("Game paused", True, (77, 97, 39))
            title_rect = title.get_rect(center=(400, 250))
            self.screen.blit(title, title_rect)

            #final_score_text = self.small_font.render("Final Score: 100", True, (77, 97, 39))
            #score_rect = final_score_text.get_rect(center=(400, 320))
            #self.screen.blit(final_score_text, score_rect)

            pygame.draw.rect(self.screen, (77, 97, 39), self.continue_button_rect)
            restart_text = self.medium_font.render("Continue", True, (211, 230, 113))
            restart_text_rect = restart_text.get_rect(center=self.continue_button_rect.center)
            self.screen.blit(restart_text, restart_text_rect)

            pygame.draw.rect(self.screen, (77, 97, 39), self.quit_button_rect)
            quit_text = self.medium_font.render("Leave", True, (211, 230, 113))
            quit_text_rect = quit_text.get_rect(center=self.quit_button_rect.center)
            self.screen.blit(quit_text, quit_text_rect)

    def handle_event(self, event):
        if self.active and event.type == pygame.MOUSEBUTTONDOWN:
            if self.continue_button_rect.collidepoint(event.pos):
                return "continue"
            if self.quit_button_rect.collidepoint(event.pos):
                return "quit"
        return None