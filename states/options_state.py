from states.base_state import State
from states.entities import Stars
import pygame

class OptionsState(State):
    def __init__(self, previous_state=None):
        self.previous_state = previous_state

    def on_enter(self, app):
        self.font = pygame.font.Font(None, 36)

        self.title_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 48)
        self.options_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 24)


        # Time for stars
        self.t = 0

        # Make the stars
        num_stars = 200
        self.stars = [Stars(app.width, app.height) for _ in range(num_stars)]
        
    def handle_event(self, app, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                if self.previous_state:
                    app.change_state(self.previous_state)
                else:
                    from states.main_menu_state import MainMenuState
                    app.change_state(MainMenuState())

    def update(self, app, dt):
        self.t += dt

    def draw(self, app, screen):
        screen.fill((0, 0, 0))

        # Draw the stars
        for star in self.stars:
            star.draw(screen, self.t)

        text = self.title_font.render("Options", True, (255, 255, 255))
        title_rect = text.get_rect(center=(app.width // 2, app.height // 5))

        options_text = self.options_font.render("Placeholder", True, (255, 255, 255))
        options_rect = options_text.get_rect(center=(app.width // 2, app.height // 2))

        screen.blit(text, title_rect)
        screen.blit(options_text, options_rect)

        back_text = self.font.render("Press ESC to go back", True, (160, 160, 160))
        back_rect = back_text.get_rect(center=(app.width // 2, app.height - 50))
        screen.blit(back_text, back_rect)