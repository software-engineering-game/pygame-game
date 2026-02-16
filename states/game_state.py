import pygame
from states.base_state import State

class GameState(State):
    def on_enter(self, app):
        self.font = pygame.font.SysFont(None, 36)

    def handle_event(self, app, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            from states.menu_state import MainMenuState
            app.change_state(MainMenuState())

    def update(self, app, dt):
        pass

    def draw(self, app, screen):
        screen.fill((10, 10, 15))
        text = self.font.render("GAME - press ESC for menu", True, (220, 220, 220))
        screen.blit(text, (30, 30))
