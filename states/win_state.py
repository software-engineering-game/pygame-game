from states.base_state import State
from states.main_menu_state import MainMenuState
from states.entities import Stars
import json
import os
import pygame

class WinState(State):
    def __init__(self, message, score):
        self.message = message
        self.score = score
        self.name = ""
        self.entering_name = True
        self.leaderboard = []

    def on_enter(self, app):
        # Time for stars
        self.t = 0

        # Make the stars
        num_stars = 200
        self.stars = [Stars(app.width, app.height) for _ in range(num_stars)]

    def handle_event(self, app, event):
        if event.type == pygame.KEYDOWN:

            if self.entering_name:
                if event.key == pygame.K_RETURN:
                    if self.name.strip() == "":
                        self.name = "AAA"

                    self.save_score()
                    self.entering_name = False

                elif event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]

                else:
                    if len(self.name) < 10:
                        self.name += event.unicode.upper()

            else:
                if event.key == pygame.K_RETURN:
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

        # sort highest first
        self.leaderboard = sorted(self.leaderboard, key=lambda x: x["score"], reverse=True)

        # keep top 5
        self.leaderboard = self.leaderboard[:5]

        # save
        with open(file_path, "w") as f:
            json.dump(self.leaderboard, f, indent=4)

    def update(self, app, dt):
        pass

    def draw(self, app, screen):
        screen.fill((0, 0, 0))

        font_big = pygame.font.Font(None, 80)
        font_small = pygame.font.Font(None, 40)

        text = font_big.render(self.message, True, (255, 255, 0))
        screen.blit(text, text.get_rect(center=(app.width // 2, app.height // 3)))

        score_text = font_small.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, score_text.get_rect(center=(app.width // 2, app.height // 2.5)))

        for star in self.stars:
            star.draw(screen, self.t)

        # Name input
        if self.entering_name:
            name_text = font_small.render(f"Enter Name: {self.name}", True, (255, 255, 255))
            screen.blit(name_text, name_text.get_rect(center=(app.width // 2, app.height // 2 + 60)))

        else:
            # Leaderboard title
            lb_title = font_small.render("Leaderboard", True, (255, 255, 0))
            screen.blit(lb_title, lb_title.get_rect(center=(app.width // 2, app.height // 2 + 40)))

            # Show scores
            for i, entry in enumerate(self.leaderboard):
                text = font_small.render(
                    f"{i+1}. {entry['name']} - {entry['score']}",
                    True,
                    (255, 255, 255)
                )
                screen.blit(text, (app.width // 2 - 100, app.height // 2 + 80 + i * 30))

            cont_text = font_small.render("Press Enter to return to menu", True, (180, 180, 180))
            screen.blit(cont_text, cont_text.get_rect(center=(app.width // 2, app.height - 50)))

    