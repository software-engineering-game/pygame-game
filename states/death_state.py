# states/death_state.py

import pygame
import json
import os
from states.base_state import State
from states.main_menu_state import MainMenuState
from states import settings
from states import utils
from states.entities import Stars


class DeathState(State):
    def __init__(self, message="You Died", score=0):
        self.message = message
        self.score = score

        self.is_new_high = False
        self.high_score = 0

        self.name = ""
        self.entering_name = True
        self.leaderboard = []

        self.title_font = "assets/fonts/PressStart2P-vaV7.ttf"
        self.score_font = "assets/fonts/PressStart2P-vaV7.ttf"
        self.info_font = "assets/fonts/PressStart2P-vaV7.ttf"

    def on_enter(self, app):
        self.title_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 72)
        self.score_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 24)
        self.info_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 14)

        self.high_score = utils.load_high_score()
        self.is_new_high = self.score > self.high_score

        # Stop music
        if hasattr(app, "music"):
            app.music.stop()

        # Time for stars
        self.t = 0

        # Make the stars
        num_stars = 200
        self.stars = [Stars(app.width, app.height) for _ in range(num_stars)]

    def on_exit(self, app):
        pass

    def handle_event(self, app, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key in (pygame.K_ESCAPE, pygame.K_q):
            app.running = False
            return

        if self.entering_name:
            if event.key == settings.keybind_menu_confirm:
                if self.name.strip() == "":
                    self.name = "AAA"

                self.save_score()
                utils.save_high_score(self.score)
                self.high_score = utils.load_high_score()

                self.entering_name = False

            elif event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]

            else:
                if len(self.name) < 10 and event.unicode.isprintable():
                    self.name += event.unicode.upper()

            return

        # After score is submitted
        if event.key == pygame.K_r or event.key == settings.keybind_menu_confirm:
            from states.game_state import GameState
            GameState.saved_player_position = None
            app.change_state(MainMenuState())

    def save_score(self):
        file_path = "leaderboard.json"

        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    content = f.read().strip()
                    if content:
                        self.leaderboard = json.loads(content)
                    else:
                        self.leaderboard = []
            except json.JSONDecodeError:
                self.leaderboard = []
        else:
            self.leaderboard = []

        self.leaderboard.append({
            "name": self.name if self.name else "AAA",
            "score": self.score
        })

        # Sort highest first
        self.leaderboard = sorted(
            self.leaderboard,
            key=lambda x: x["score"],
            reverse=True
        )

        # Keep top 5
        self.leaderboard = self.leaderboard[:5]

        with open(file_path, "w") as f:
            json.dump(self.leaderboard, f, indent=4)

    def update(self, app, dt):
        self.t += dt

    def draw(self, app, screen):
        screen.fill((0, 0, 0))

        cx = settings.WIDTH // 2
        cy = settings.HEIGHT // 2

        for star in self.stars:
            star.draw(screen, self.t)

        title = self.title_font.render(self.message, True, (255, 0, 0))
        title_rect = title.get_rect(center=(cx, cy - 170))
        screen.blit(title, title_rect)

        score_text = self.score_font.render(f"Score: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(cx, cy - 80))
        screen.blit(score_text, score_rect)

        if self.is_new_high:
            high_text = self.score_font.render("New High Score!", True, (255, 255, 0))
        else:
            high_text = self.score_font.render(f"Best: {self.high_score}", True, (180, 180, 180))

        high_rect = high_text.get_rect(center=(cx, cy - 35))
        screen.blit(high_text, high_rect)

        if self.entering_name:
            name_text = self.score_font.render(f"Name: {self.name}", True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(cx, cy + 35))
            screen.blit(name_text, name_rect)

            info = self.info_font.render("Press Enter to Submit | Q or ESC to Quit", True, (180, 180, 180))
            info_rect = info.get_rect(center=(cx, cy + 90))
            screen.blit(info, info_rect)

        else:
            lb_title = self.score_font.render("Leaderboard", True, (255, 255, 0))
            lb_title_rect = lb_title.get_rect(center=(cx, cy + 20))
            screen.blit(lb_title, lb_title_rect)

            for i, entry in enumerate(self.leaderboard):
                entry_text = self.info_font.render(
                    f"{i + 1}. {entry['name']} - {entry['score']}",
                    True,
                    (255, 255, 255)
                )
                entry_rect = entry_text.get_rect(center=(cx, cy + 60 + i * 28))
                screen.blit(entry_text, entry_rect)

            info = self.info_font.render("Press Enter or R to Menu | Q or ESC to Quit", True, (180, 180, 180))
            info_rect = info.get_rect(center=(cx, settings.HEIGHT - 40))
            screen.blit(info, info_rect)