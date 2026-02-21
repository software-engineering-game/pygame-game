import pygame
from states.base_state import State
from states import settings

# Pause Screen Class
class PauseScreen(State):
    def __init__(self, app, previous_state):
        self.app = app
        self.previous_state = previous_state
        self.screen = app.screen
        self.font = pygame.font.Font(None, 74)
        self.resume_button = pygame.Rect(settings.WIDTH // 2 - 100, settings.HEIGHT // 2, 200, 50)
        self.quit_button = pygame.Rect(settings.WIDTH // 2 - 100, settings.HEIGHT // 2 + 70, 200, 50)

    def draw(self, app, screen):
        # Draw the pause message
        pause_text = self.font.render("Paused", True, (255, 255, 0))
        text_rect = pause_text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 - 100))
        screen.blit(pause_text, text_rect)

        # Draw the resume button
        pygame.draw.rect(self.screen, (0, 255, 0), self.resume_button)
        resume_text = self.font.render("Resume", True, (0, 0, 0))
        resume_text_rect = resume_text.get_rect(center=self.resume_button.center)
        screen.blit(resume_text, resume_text_rect)

        # Draw the quit button
        pygame.draw.rect(self.screen, (255, 0, 0), self.quit_button)
        quit_text = self.font.render("Quit", True, (0, 0, 0))
        quit_text_rect = quit_text.get_rect(center=self.quit_button.center)
        screen.blit(quit_text, quit_text_rect)

    def handle_event(self, app, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            app.change_state(self.previous_state)
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.resume_button.collidepoint(event.pos):
                app.change_state(self.previous_state)
                return
            elif self.quit_button.collidepoint(event.pos):
                app.running = False
                return
    
    def update(self, app, dt):
        pass
