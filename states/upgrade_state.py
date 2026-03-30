
import pygame
from states.base_state import State
from states.main_menu_state import MainMenuState
from states import settings
from states import utils

class UpgradeState(State):
    def __init__(self, app, previous_state):
        self.previous_state = previous_state

    def on_enter(self, app):
        self.font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 32)
        self.small_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 24)

        self.selected = 0
        self.options = ["Faster Bullet Speed", "Faster Cooldown"]

    def handle_event(self, app, event):
        sfx_menu = pygame.mixer.Sound("assets/sfx/menu1.wav")
        if event.type == pygame.KEYDOWN:

            if event.key in (pygame.K_UP, pygame.K_DOWN):
                self.selected = (self.selected + 1) % 2
                pygame.mixer.Sound.play(sfx_menu)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.selected == 0:
                    settings.BULLET_SPEED = 15
                    app.change_state(self.previous_state)
                else:
                    settings.BULLET_COOLDOWN = 0.1
                    app.change_state(self.previous_state)
            elif event.key == pygame.K_ESCAPE:
                app.change_state(self.previous_state)

    def update(self, app, dt):
        pass

    def draw(self, app, screen):

        self.previous_state.draw(app, screen)

        overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        text = self.font.render("Choose an Upgrade:", True, (255, 255, 255))
        rect = text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 - 80))
        screen.blit(text, rect)

        for i, option in enumerate(self.options):

            color = (255, 255, 0) if i == self.selected else (180, 180, 180)
            opt = self.small_font.render(option, True, color)

            opt_rect = opt.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 + (i * 60)))
            screen.blit(opt, opt_rect)
