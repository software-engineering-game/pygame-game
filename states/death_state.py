# states/death_state.py

import pygame
from states.base_state import State
from states.main_menu_state import MainMenuState
from states import settings


class DeathState(State):
    def __init__(self, message="You Died"):
        self.message = message
        self.title_font = None
        self.info_font = None

    def on_enter(self, app):
        #ADDED: load fonts when entering death screen
        self.title_font = pygame.font.Font(None, 96)
        self.info_font = pygame.font.Font(None, 36)

    def on_exit(self, app):
        # Nothing to clean up right now
        pass

    def handle_event(self, app, event):
    # ADDED: controls for death screen
        if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_r:
            #ADDED: reset saved player position so new game starts fresh
            from states.game_state import GameState
            GameState.saved_player_position = None

            app.change_state(MainMenuState())
        elif event.key in (pygame.K_ESCAPE, pygame.K_q):
            app.running = False

    def update(self, app, dt):
        # No updates needed for a static screen
        pass

    def draw(self, app, screen):
        #ADDED: draw death screen
        screen.fill((0, 0, 0))

        title = self.title_font.render(self.message, True, (255, 0, 0))
        title_rect = title.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 - 40))
        screen.blit(title, title_rect)

        info = self.info_font.render("Press R to go to Menu | Press Q or ESC to Quit", True, (255, 255, 255))
        info_rect = info.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 + 40))
        screen.blit(info, info_rect)