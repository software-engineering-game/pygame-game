# states/death_state.py

import pygame
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
        self.title_font = "assets/fonts/PressStart2P-vaV7.ttf"
        self.score_font = "assets/fonts/PressStart2P-vaV7.ttf"
        self.info_font = "assets/fonts/PressStart2P-vaV7.ttf"

    def on_enter(self, app):
        self.title_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 72)
        self.score_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 24)
        self.info_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 14)

        self.is_new_high = utils.save_high_score(self.score)
        self.high_score = utils.load_high_score()

        #stop music
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
        
        if event.key == pygame.K_r:
            from states.game_state import GameState
            GameState.saved_player_position = None
            app.change_state(MainMenuState())

        elif event.key in (pygame.K_ESCAPE, pygame.K_q):
            app.running = False

    def update(self, app, dt):
        pass

    def draw(self, app, screen):
        screen.fill((0, 0, 0))
        cx = settings.WIDTH // 2
        cy = settings.HEIGHT // 2

        title = self.title_font.render(self.message, True, (255, 0, 0))
        title_rect = title.get_rect(center=(cx, cy - 80))
        screen.blit(title, title_rect)

        score_text = self.score_font.render(f"Score: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(cx, cy))
        screen.blit(score_text, score_rect)

        if self.is_new_high:
            high_text = self.score_font.render("New High Score!", True, (255, 255, 0))
        else:
            high_text = self.score_font.render(f"Best: {self.high_score}", True, (180, 180, 180))
        high_rect = high_text.get_rect(center=(cx, cy + 50))
        screen.blit(high_text, high_rect)

        info = self.info_font.render("Press R to go to Menu | Press Q or ESC to Quit", True, (255, 255, 255))
        info_rect = info.get_rect(center=(cx, cy + 110))
        screen.blit(info, info_rect)

        for star in self.stars:
            star.draw(screen, self.t)