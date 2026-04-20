import pygame
from states.base_state import State
from states import settings
from states.main_menu_state import MainMenuState

# Pause Screen Class
class PauseScreen(State):
    def __init__(self, app, previous_state):
        self.selected_index = 0
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

        resume_color = (255, 255, 0) if self.selected_index == 0 else (175, 175, 175)
        main_color = (255, 255, 0) if self.selected_index == 1 else (175, 175, 175)
        quit_color = (255, 255, 0) if self.selected_index == 2 else (175, 10, 10)

        # Draw the resume button
        pygame.draw.rect(screen, resume_color, self.resume_button)
        resume_text = self.font_resume.render("Resume", True, (0, 0, 0))
        resume_text_rect = resume_text.get_rect(center=self.resume_button.center)
        screen.blit(resume_text, resume_text_rect)

        # Draw the Main menu button button
        pygame.draw.rect(screen, main_color, self.main_menu_button)
        main_menu_text = self.font_main_menu.render("Main Menu", True, (0, 0, 0))
        main_menu_text_rect = main_menu_text.get_rect(center=self.main_menu_button.center)
        screen.blit(main_menu_text, main_menu_text_rect)

        # Draw the quit button
        pygame.draw.rect(screen, quit_color, self.quit_button)
        quit_text = self.font_quit.render("Quit", True, (0, 0, 0))
        quit_text_rect = quit_text.get_rect(center=self.quit_button.center)
        screen.blit(quit_text, quit_text_rect)

    def handle_event(self, app, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                app.state = self.previous_state
                return

            elif event.key in (pygame.K_UP, pygame.K_w):
                self.selected_index = (self.selected_index - 1) % 3

            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_index = (self.selected_index + 1) % 3

            elif event.key in (pygame.K_RETURN, settings.keybind_menu_confirm):
                if self.selected_index == 0:
                    app.state = self.previous_state
                    return

                elif self.selected_index == 1:
                    app.change_state(MainMenuState())
                    return

                elif self.selected_index == 2:
                    from states.confirm_quit_state import ConfirmQuitState
                    app.change_state(ConfirmQuitState(self))
                    return
        
    def update(self, app, dt):
        pass
