import pygame
from states.base_state import State
from states.entities import Stars
from states import utils

class MainMenuState(State):

    def on_enter(self, app):
        # Time for stars
        self.t = 0

        # Make the stars
        num_stars = 200
        self.stars = [Stars(app.width, app.height) for _ in range(num_stars)]

        # Fonts
        self.title_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 48)
        self.menu_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 24)
        self.score_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 16)
        

        self.high_score = utils.load_high_score()

        # Menu options
        self.options = ["Start Game", "How To Play", "Options", "Credits", "Quit"]
        
        if not hasattr(self, "selected"):
            self.selected = 0

    def handle_event(self, app, event):
        sfx_menu = pygame.mixer.Sound("assets/sfx/menu1.wav")
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
                pygame.mixer.Sound.play(sfx_menu)

            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
                pygame.mixer.Sound.play(sfx_menu)

            elif event.key == pygame.K_RETURN:

                if self.selected == 0:
                    from states.game_state import GameState
                    app.change_state(GameState())

                elif self.selected == 1:
                    from states.how_to_play_state import HowToPlayState
                    app.change_state(HowToPlayState(self))

                elif self.selected == 2:
                    from states.options_state import OptionsState
                    app.change_state(OptionsState(self))

                elif self.selected == 3:
                    from states.credits_state import CreditsState
                    app.change_state(CreditsState(self))

                elif self.selected == 4:
                    from states.confirm_quit_state import ConfirmQuitState
                    app.change_state(ConfirmQuitState(self))


            elif event.key == pygame.K_ESCAPE:
                from states.confirm_quit_state import ConfirmQuitState
                app.change_state(ConfirmQuitState(self))

    def update(self, app, dt):
        self.t += dt

    def draw(self, app, screen):
        # Background
        screen.fill((0, 0, 0))

        # Draw the stars
        for star in self.stars:
            star.draw(screen, self.t)

        # Title
        title_text = self.title_font.render("Space Dodgers", True, (255, 255, 0))
        title_rect = title_text.get_rect(center=(app.width // 2, app.height // 5))
        screen.blit(title_text, title_rect)

        # High score below title
        if self.high_score > 0:
            hs_text = self.score_font.render(f"High Score: {self.high_score}", True, (255, 215, 0))
            hs_rect = hs_text.get_rect(center=(app.width // 2, app.height // 5 + 50))
            screen.blit(hs_text, hs_rect)

        # Menu nav
        menu_top = app.height // 3
        x = 60
        line_height = 60

        for i, option in enumerate(self.options):
            y = menu_top + 40 + i * line_height

            if i == self.selected:
                prefix = "> "
                color = (255, 255, 255)
            else:
                prefix = "  "
                color = (160, 160, 160)
            
            text = self.menu_font.render(prefix + option, True, color)
            screen.blit(text, (x, y))

        
