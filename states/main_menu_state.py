import pygame
import random
import math
from states.base_state import State

class Stars:
    def __init__(self, w, h):
        self.x = random.randint(0, w - 1)
        self.y = random.randint(0, h - 1)
        self.r = random.choice([1, 1, 1, 2])
        self.base = random.randint(120, 120)
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
        self.stars = [Stars(app.width, app.height) for _ in range(200)]

        # Fonts
        self.title_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 48)
        self.menu_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 24)

        # Menu options
        self.options = ["Start Game", "Quit"]
        self.selected = 0

    def handle_event(self, app, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)

            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)

            elif event.key == pygame.K_RETURN:

                if self.selected == 0:
                    from states.game_state import GameState
                    app.change_state(GameState())

                elif self.selected == 1:
                    app.running = False

            elif event.key == pygame.K_ESCAPE:
                app.running = False

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

        
