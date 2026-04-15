import pygame
from states.base_state import State
from states import settings
from states.main_menu_state import MainMenuState

button_color_resume = (175, 175, 175)
button_color_main = (175, 175, 175)
button_color_quit = (175, 10, 10)

# Pause Screen Class
class PauseScreen(State):
    def __init__(self, app, previous_state):
        self.app = app
        self.previous_state = previous_state
        self.screen = app.screen

        self.font_pause = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 54)
        self.font_resume = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 28)
        self.font_main_menu = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 20)
        self.font_quit = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 34)
        
        self.resume_button = pygame.Rect(settings.WIDTH // 2 - 100, settings.HEIGHT // 2 - 70, 200, 50)
        self.main_menu_button = pygame.Rect(settings.WIDTH // 2 - 100, settings.HEIGHT // 2, 200, 50)
        self.quit_button = pygame.Rect(settings.WIDTH // 2 - 100, settings.HEIGHT // 2 + 70, 200, 50)

    def draw(self, app, screen):
        # Draw the pause message
        pause_text = self.font_pause.render("Paused", True, (255, 255, 0))
        text_rect = pause_text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 - 120))
        screen.blit(pause_text, text_rect)

        # Draw the resume button
        pygame.draw.rect(self.screen, button_color_resume, self.resume_button)
        resume_text = self.font_resume.render("Resume", True, (0, 0, 0))
        resume_text_rect = resume_text.get_rect(center=self.resume_button.center)
        screen.blit(resume_text, resume_text_rect)

        # Draw the Main menu button button
        pygame.draw.rect(self.screen, button_color_main, self.main_menu_button)
        main_menu_text = self.font_main_menu.render("Main Menu", True, (0, 0, 0))
        main_menu_text_rect = main_menu_text.get_rect(center=self.main_menu_button.center)
        screen.blit(main_menu_text, main_menu_text_rect)

        # Draw the quit button
        pygame.draw.rect(self.screen, button_color_quit, self.quit_button)
        quit_text = self.font_quit.render("Quit", True, (0, 0, 0))
        quit_text_rect = quit_text.get_rect(center=self.quit_button.center)
        screen.blit(quit_text, quit_text_rect)

    def handle_event(self, app, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                #ADDED: resume without re-running GameState.on_enter()
                app.state = self.previous_state
                return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.resume_button.collidepoint(event.pos):
                  #ADDED: resume without re-running GameState.on_enter()
                    app.state = self.previous_state
                    return
            elif self.quit_button.collidepoint(event.pos):
                from states.confirm_quit_state import ConfirmQuitState
                app.change_state(ConfirmQuitState(self))
                return
            elif self.main_menu_button.collidepoint(event.pos):
                app.change_state(MainMenuState())
    
    def update(self, app, dt):
        pass
