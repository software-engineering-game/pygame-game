import pygame
import random
import math
from states.base_state import State

class Stars:
    def __init__(self, w, h):
        self.x = random.randint(0, w - 1)
        self.y = random.randint(0, h - 1)
        self.r = random.choice([1, 1, 1, 2])
        self.base = random.randint(100, 180)
        self.amp = random.randint(20, 80)
        self.speed = random.uniform(1.0, 4.0)
        self.phase = random.uniform(0, math.tau)

    def brightness(self, t):
        b = self.base + self.amp * math.sin(t * self.speed + self.phase)
        return max(0, min(255, int(b)))
    
    def draw(self, screen, t):
        b = self.brightness(t)
        pygame.draw.circle(screen, (b, b, b), (self.x, self.y), self.r)


class MainMenuState(State):

    def on_enter(self, app):
        # Time for stars
        self.t = 0

        # Make the stars
        num_stars = 200
        self.stars = [Stars(app.width, app.height) for _ in range(num_stars)]

        # Fonts
        self.title_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 48)
        self.menu_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 24)

        # Menu options
        self.options = ["Start Game", "How To Play", "Options", "Credits", "Quit"]
        
        if not hasattr(self, "selected"):
            self.selected = 0

    def handle_event(self, app, event):
        sfx_menu = pygame.mixer.Sound("assets/sfx/menu1.wav")
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
                pygame.mixer.Sound.play(sfx_menu)

            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
                pygame.mixer.Sound.play(sfx_menu)

            elif event.key == pygame.K_RETURN:

                if self.selected == 0:
                    from states.game_state import GameState
                    app.change_state(GameState())

                elif self.selected == 1:
                    from states.how_to_play_state import HowToPlayState
                    app.change_state(HowToPlayState(self))

                elif self.selected == 2:
                    from states.options_state import OptionsState
                    app.change_state(OptionsState(self))

                elif self.selected == 3:
                    from states.credits_state import CreditsState
                    app.change_state(CreditsState(self))

                elif self.selected == 4:
                    from states.confirm_quit_state import ConfirmQuitState
                    app.change_state(ConfirmQuitState(self))


            elif event.key == pygame.K_ESCAPE:
                from states.confirm_quit_state import ConfirmQuitState
                app.change_state(ConfirmQuitState(self))

    def update(self, app, dt):
        self.t += dt

    def draw(self, app, screen):
        # Background
        screen.fill((0, 0, 0))

        # Draw the stars
        for star in self.stars:
            star.draw(screen, self.t)

        # Title
        title_text = self.title_font.render("Space Dodgers", True, (255, 255, 0))
        title_rect = title_text.get_rect(center=(app.width // 2, app.height // 5))
        screen.blit(title_text, title_rect)

        # Menu nav
        menu_top = app.height // 3
        x = 60
        line_height = 60

        for i, option in enumerate(self.options):
            y = menu_top + 40 + i * line_height

            if i == self.selected:
                prefix = "> "
                color = (255, 255, 255)
            else:
                prefix = "  "
                color = (160, 160, 160)
            
            text = self.menu_font.render(prefix + option, True, color)
            screen.blit(text, (x, y))

        
