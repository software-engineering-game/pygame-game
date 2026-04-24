
import pygame
from states.base_state import State
from states import settings

class UpgradeState(State):
    def __init__(self, app, previous_state):
        self.previous_state = previous_state

    def on_enter(self, app):
        self.font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 32)
        self.small_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 20)
        self.tiny_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 16)

        self.selected = 0
        self.options = ["Bullet Speed +2", "Fire Rate +10%"]

    def handle_event(self, app, event):
        sfx_menu = pygame.mixer.Sound("assets/sfx_ogg/menu1.ogg")
        if event.type == pygame.KEYDOWN:

            if event.key in (pygame.K_UP, pygame.K_DOWN):
                self.selected = (self.selected + 1) % 2
                pygame.mixer.Sound.play(sfx_menu)
            elif event.key == settings.keybind_menu_confirm:
                if self.selected == 0:
                    settings.bullet_spd = min(25, settings.bullet_spd + 2)
                    self._resume_previous_state(app)
                else:
                    settings.bullet_cooldown = max(0.05, settings.bullet_cooldown * 0.9)
                    self._resume_previous_state(app)
            elif event.key == pygame.K_ESCAPE:
                self._resume_previous_state(app)

    def _resume_previous_state(self, app):
        if hasattr(self.previous_state, "on_upgrade_complete"):
            self.previous_state.on_upgrade_complete()
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
        rect = text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 - 100))
        screen.blit(text, rect)

        stats_text = self.tiny_font.render(
            f"bullet speed: {settings.bullet_spd}   cooldown: {settings.bullet_cooldown:.2f}s",
            True,
            (200, 200, 200)
        )
        stats_rect = stats_text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 - 20))
        screen.blit(stats_text, stats_rect)

        for i, option in enumerate(self.options):

            color = (255, 255, 0) if i == self.selected else (180, 180, 180)
            opt = self.small_font.render(option, True, color)

            opt_rect = opt.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 + 55 + (i * 60)))
            screen.blit(opt, opt_rect)
