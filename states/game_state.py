import pygame
from states.base_state import State
from states.menu_state import MenuState

class GameState(State):
    def on_enter(self, app):
        self.font = pygame.font.Font(None, 36)

    def handle_event(self, app, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            app.change_state(MenuState())

    def update(self, app, dt):
        pass

    def draw(self, app, screen):
        screen.fill((10, 10, 15))
        text = self.font.render("GAME - press ESC for menu", True, (220, 220, 220))
        screen.blit(text, (30, 30))
