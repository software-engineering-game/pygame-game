import pygame
from states import settings
from states import utils
from states.base_state import State


class PlayCustomSelectState(State):
    def __init__(self, previous_state=None):
        self.previous_state = previous_state

    def on_enter(self, app):
        self.menu_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 22)
        self.title_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 28)
        self.small_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 16)

        self.paths = utils.list_valid_custom_level_paths()
        self.selected = 0

    def handle_event(self, app, event):
        if event.type != pygame.KEYDOWN:
            return

        sfx_menu = pygame.mixer.Sound("assets/sfx_ogg/menu1.ogg")

        def play_menu():
            if settings.SFX_ON:
                pygame.mixer.Sound.play(sfx_menu)

        if event.key == pygame.K_ESCAPE:
            from states.main_menu_state import MainMenuState

            app.change_state(MainMenuState())
            return

        if not self.paths:
            if event.key == settings.keybind_menu_confirm:
                from states.main_menu_state import MainMenuState

                app.change_state(MainMenuState())
                play_menu()
            return

        if event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % len(self.paths)
            play_menu()
        elif event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % len(self.paths)
            play_menu()
        elif event.key == settings.keybind_menu_confirm:
            from states.game_state import GameState

            path = self.paths[self.selected]
            app.change_state(GameState(custom_level_path=path))
            play_menu()

    def update(self, app, dt):
        pass

    def draw(self, app, screen):
        screen.fill((12, 12, 28))
        title = self.title_font.render("Play Custom Level", True, (255, 255, 120))
        screen.blit(title, (40, 28))

        if not self.paths:
            msg = self.menu_font.render(
                "No custom levels yet.",
                True,
                (220, 220, 240),
            )
            screen.blit(msg, (40, 120))
            hint = self.small_font.render(
                "Create one in Make Level, then save to a slot.",
                True,
                (160, 160, 180),
            )
            screen.blit(hint, (40, 168))
            back = self.small_font.render(
                "Enter or Esc: back to menu",
                True,
                (140, 140, 160),
            )
            screen.blit(back, (40, app.height - 48))
            return

        y = 100
        for i, path in enumerate(self.paths):
            label = utils.friendly_name_for_custom_path(path)
            sel = i == self.selected
            prefix = "> " if sel else "  "
            color = (255, 255, 255) if sel else (170, 170, 190)
            line = self.menu_font.render(prefix + label, True, color)
            screen.blit(line, (40, y))
            y += 40

        hint = self.small_font.render(
            "Up/Down: choose  Enter: play  Esc: menu",
            True,
            (140, 140, 160),
        )
        screen.blit(hint, (40, app.height - 48))
