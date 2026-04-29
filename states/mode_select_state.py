import pygame
from states.base_state import State
from states import settings
from states.entities import Stars


class ModeSelectState(State):
    def __init__(self):
        self.t = 0
        self.selected = 0
        self.options = ["Normal Mode", "Endless Mode", "Back"]
        self.stars = []

    def on_enter(self, app):
        self.font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 36)
        self.small_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 22)

        num_stars = 200
        self.stars = [Stars(app.width, app.height) for _ in range(num_stars)]

    def handle_event(self, app, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % len(self.options)

        elif event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % len(self.options)

        elif event.key == settings.keybind_menu_confirm:
            if self.selected == 0:
                from states.game_state import GameState
                app.change_state(GameState())

            elif self.selected == 1:
                from states.endless_game_state import EndlessGameState
                app.change_state(EndlessGameState())

            elif self.selected == 2:
                from states.main_menu_state import MainMenuState
                app.change_state(MainMenuState())

        elif event.key == pygame.K_ESCAPE:
            from states.main_menu_state import MainMenuState
            app.change_state(MainMenuState())

    def update(self, app, dt):
        self.t += dt

    def draw(self, app, screen):
        screen.fill((0, 0, 0))

        for star in self.stars:
            star.draw(screen, self.t)

        title = self.font.render("Select Mode", True, (255, 255, 255))
        title_rect = title.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 - 140))
        screen.blit(title, title_rect)

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (180, 180, 180)
            text = self.small_font.render(option, True, color)
            rect = text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 - 40 + i * 60))
            screen.blit(text, rect)