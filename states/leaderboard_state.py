from states.base_state import State
from states.main_menu_state import MainMenuState
from states.entities import Stars
import pygame
import json
import os

class LeaderboardState(State):
    def __init__(self):
        self.leaderboard = []

    def on_enter(self, app):
        # star background
        self.t = 0
        self.stars = [Stars(app.width, app.height) for _ in range(200)]

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

        # keep top 10
        self.leaderboard = sorted(self.leaderboard, key=lambda x: x["score"], reverse=True)[:10]

    def handle_event(self, app, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                app.change_state(MainMenuState())

    def update(self, app, dt):
        self.t += dt

    def draw(self, app, screen):
        screen.fill((0, 0, 0))

        # stars
        for star in self.stars:
            star.draw(screen, self.t)

        font_big = pygame.font.Font(None, 80)
        font_small = pygame.font.Font(None, 40)

        # title
        title = font_big.render("Leaderboard", True, (255, 255, 0))
        screen.blit(title, title.get_rect(center=(app.width // 2, app.height // 6)))

        # entries
        start_y = app.height // 3

        for i, entry in enumerate(self.leaderboard):
            text = font_small.render(
                f"{i+1}. {entry['name']} - {entry['score']}",
                True,
                (255, 255, 255)
            )
            screen.blit(text, text.get_rect(center=(app.width // 2, start_y + i * 40)))

        # bottom text
        bottom = font_small.render("Press ESC to go back", True, (180, 180, 180))
        screen.blit(bottom, bottom.get_rect(center=(app.width // 2, app.height - 50)))