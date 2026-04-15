from states.base_state import State
import random
import math
import pygame

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


class CreditsState(State):
    def __init__(self, previous_state=None):
        self.previous_state = previous_state

    def on_enter(self, app):
        self.font = pygame.font.Font(None, 36)

        self.title_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 48)
        self.names_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 20)

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

        title_text = self.title_font.render("Credits", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(app.width // 2, app.height // 5))

        lines = [
            "Dev Team:",
            "Nicholas Vuletich, Ian Scheetz,",
            "Crawford Barnett, Mayah Nix,",
            "Samaa Hediya, Ayush Patel, Bishal Regmi",
            "",
            "Audio Programming and Design:",
            "Ian Scheetz",
            "",
            "Artist:",
            "Thomas Bond"
        ]

        y_start = (app.height // 2) - 120
        line_spacing = 35

        for i, line in enumerate(lines):
            names_text = self.names_font.render(line, True, (255, 255, 255))
            names_rect = names_text.get_rect(center=(app.width // 2, y_start + i * line_spacing))
            screen.blit(names_text, names_rect)

        back_text = self.font.render("Press ESC to go back", True, (160, 160, 160))
        back_rect = back_text.get_rect(center=(app.width // 2, app.height - 50))
        
        screen.blit(back_text, back_rect)
        screen.blit(title_text, title_rect)