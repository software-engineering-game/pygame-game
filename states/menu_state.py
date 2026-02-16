import pygame
from states.base_state import State
from states.game_state import GameState

class MainMenuState(State):
    def on_enter(self, app):
        self.font = pygame.font.Font(None, 48)

    def handle_event(self, app, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                app.change_state(GameState())
            elif event.key == pygame.K_ESCAPE:
                app.running = False

    def update(self, app, dt):
        pass

    def draw(self, app, screen):
        screen.fill((0, 0, 0))
        text = self.font.render("MENU - press ENTER", True, (255, 255, 255))
        screen.blit(text, (app.width // 2 - text.get_width() // 2, app.height // 2))
