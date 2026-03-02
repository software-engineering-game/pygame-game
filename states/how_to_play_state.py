from states.base_state import State
from states import settings
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


class HowToPlayState(State):
    def __init__(self, previous_state=None):
        self.previous_state = previous_state

    def on_enter(self, app):
        self.title_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 48)
        self.controls_img = pygame.image.load("assets/controls.png").convert_alpha()
        
        scale = 0.6
        w = int(self.controls_img.get_width() * scale)
        h = int(self.controls_img.get_height() * scale)

        self.controls_img = pygame.transform.smoothscale(self.controls_img, (w, h))   

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

        text = self.title_font.render("How To Play", True, (255, 255, 255))
        title_rect = text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 5))

        img_rect = self.controls_img.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 + 70))

        screen.blit(text, title_rect)
        screen.blit(self.controls_img, img_rect)