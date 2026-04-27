
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
        self.options = [
            "Bullet Speed +2",
            "Fire Rate +10%",
            "Extra Life +1",
            "Triple Shot",
            "Front + Back Shot"
        ]

    def handle_event(self, app, event):
        sfx_menu = pygame.mixer.Sound("assets/sfx_ogg/menu1.ogg")
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
                pygame.mixer.Sound.play(sfx_menu)

            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
                pygame.mixer.Sound.play(sfx_menu)
            elif event.key == settings.keybind_menu_confirm:
                self.apply_upgrade()
                self._resume_previous_state(app)
            elif event.key == pygame.K_ESCAPE:
                self._resume_previous_state(app)

    def apply_upgrade(self):
        selected_upgrade = self.options[self.selected]

        if selected_upgrade == "Bullet Speed +2":
            settings.bullet_spd = min(25, settings.bullet_spd + 2)

        elif selected_upgrade == "Fire Rate +10%":
            settings.bullet_cooldown = max(0.05, settings.bullet_cooldown * 0.9)

        elif selected_upgrade == "Extra Life +1":
            self.previous_state.lives += 1

        elif selected_upgrade == "Triple Shot":
            self.previous_state.player.shot_mode = "triple"
            self.previous_state.player_shot_mode = "triple"

        elif selected_upgrade == "Front + Back Shot":
            self.previous_state.player.shot_mode = "front_back"
            self.previous_state.player_shot_mode = "front_back"


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
        rect = text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 - 120))
        screen.blit(text, rect)

        current_shot = getattr(self.previous_state.player, "shot_mode", "single")

        stats_text_1 = self.tiny_font.render(
            f"speed: {settings.bullet_spd}   cooldown: {settings.bullet_cooldown:.2f}s",
            True,
            (200, 200, 200)
        )

        stats_text_2 = self.tiny_font.render(
            f"lives: {self.previous_state.lives}   shot: {current_shot}",
            True,
            (200, 200, 200)
        )

        stats_rect_1 = stats_text_1.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 - 90))
        stats_rect_2 = stats_text_2.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 - 65))

        screen.blit(stats_text_1, stats_rect_1)
        screen.blit(stats_text_2, stats_rect_2)

        for i, option in enumerate(self.options):

            color = (255, 255, 0) if i == self.selected else (180, 180, 180)
            opt = self.small_font.render(option, True, color)

            opt_rect = opt.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 + 20 + (i * 45)))
            screen.blit(opt, opt_rect)
