from states.base_state import State
from states.entities import Stars
from states import settings
import pygame


class OptionsState(State):
    def __init__(self, previous_state=None):
        self.previous_state = previous_state

    def on_enter(self, app):
        self.font = pygame.font.Font(None, 30)
        self.title_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 48)
        self.options_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 24)

        # Time for stars
        self.t = 0

        # Make the stars
        num_stars = 200
        self.stars = [Stars(app.width, app.height) for _ in range(num_stars)]

        # Menu setup
        self.selected_index = 0
        self.menu_items = ["Controls", "Sound Effects", "Music"]

    def go_back(self, app):
        if self.previous_state:
            app.change_state(self.previous_state)
        else:
            from states.main_menu_state import MainMenuState
            app.change_state(MainMenuState())

    def toggle_selected_option(self):
        current_item = self.menu_items[self.selected_index]

        if current_item == "Controls":
            if settings.CONTROL_SCHEME == "ARROWS":
                settings.CONTROL_SCHEME = "WASD"
                settings.keybind_player_up = pygame.K_w
                settings.keybind_player_down = pygame.K_s
                settings.keybind_player_left = pygame.K_a
                settings.keybind_player_right = pygame.K_d
            else:
                settings.CONTROL_SCHEME = "ARROWS"
                settings.keybind_player_up = pygame.K_UP
                settings.keybind_player_down = pygame.K_DOWN
                settings.keybind_player_left = pygame.K_LEFT
                settings.keybind_player_right = pygame.K_RIGHT

        elif current_item == "Sound Effects":
            settings.SFX_ON = not settings.SFX_ON

        elif current_item == "Music":
            settings.MUSIC_ON = not settings.MUSIC_ON

            if pygame.mixer.get_init():
                if settings.MUSIC_ON:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()

    def handle_event(self, app, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                self.go_back(app)

            elif event.key in (pygame.K_UP, pygame.K_w):
                self.selected_index = (self.selected_index - 1) % len(self.menu_items)

            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_index = (self.selected_index + 1) % len(self.menu_items)

            elif event.key in (
                pygame.K_LEFT,
                pygame.K_RIGHT,
                pygame.K_RETURN,
                pygame.K_SPACE,
                pygame.K_a,
                pygame.K_d,
            ):
                self.toggle_selected_option()

    def update(self, app, dt):
        self.t += dt

    def draw(self, app, screen):
        screen.fill((0, 0, 0))

        # Draw the stars
        for star in self.stars:
            star.draw(screen, self.t)

        # Title
        title_text = self.title_font.render("Options", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(app.width // 2, app.height // 5))
        screen.blit(title_text, title_rect)

        # Option values
        option_values = [
            f"Controls: {settings.CONTROL_SCHEME}",
            f"Sound Effects: {'ON' if settings.SFX_ON else 'OFF'}",
            f"Music: {'ON' if settings.MUSIC_ON else 'OFF'}",
        ]

        start_y = app.height // 2 - 50
        spacing = 55

        for i, text in enumerate(option_values):
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            option_surface = self.options_font.render(text, True, color)
            option_rect = option_surface.get_rect(center=(app.width // 2, start_y + i * spacing))
            screen.blit(option_surface, option_rect)

        back_text = self.font.render(
            "UP/DOWN = Select   LEFT/RIGHT/ENTER = Change   ESC = Back",
            True,
            (160, 160, 160)
        )
        back_rect = back_text.get_rect(center=(app.width // 2, app.height - 50))
        screen.blit(back_text, back_rect)