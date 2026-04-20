import pygame
from states import settings
from states.base_state import State
from states.entities import Stars
from states import utils

class MainMenuState(State):
    def on_enter(self, app):
        # Time for stars
        self.t = 0

        #stop game music
        if hasattr(app, "music"):
            pygame.mixer.music.fadeout(500)

        # Make the stars
        num_stars = 200
        self.stars = [Stars(app.width, app.height) for _ in range(num_stars)]

        # Logo Image
        self.logo_image = pygame.image.load("assets/logo.png")
        self.logo_image.set_colorkey(utils.SHEET_BG)

        # Fonts
        self.title_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 48)
        self.menu_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 24)
        self.score_font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 16)

        #mixer initializer
        pygame.mixer.init(devicename="pygame.mixer.get_dev_info()")

        self.high_score = utils.load_high_score()

        # Menu options
        self.options = ["Start Game", "Leaderboard", "How To Play", "Options", "Credits", "Quit"]
        
        if not hasattr(self, "selected"):
            self.selected = 0

    def handle_event(self, app, event):
        sfx_menu = pygame.mixer.Sound("assets/sfx_ogg/menu1.ogg")
        if event.type == pygame.KEYDOWN:

            # Switching Selection
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
                if settings.SFX_ON:
                    pygame.mixer.Sound.play(sfx_menu)

            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
                if settings.SFX_ON:    
                    pygame.mixer.Sound.play(sfx_menu)

            # Confirming Menu Selection
            elif event.key == settings.keybind_menu_confirm:

                if self.selected == 0:
                    from states.game_state import GameState
                    app.change_state(GameState())

                elif self.selected == 1:
                    from states.leaderboard_state import LeaderboardState
                    app.change_state(LeaderboardState())

                elif self.selected == 2:
                    from states.how_to_play_state import HowToPlayState
                    app.change_state(HowToPlayState(self))

                elif self.selected == 3:
                    from states.options_state import OptionsState
                    app.change_state(OptionsState(self))

                elif self.selected == 4:
                    from states.credits_state import CreditsState
                    app.change_state(CreditsState(self))
                
                elif self.selected == 5:
                    from states.confirm_quit_state import ConfirmQuitState
                    app.change_state(ConfirmQuitState(self))

            # Exiting Menu
            elif event.key == settings.keybind_menu_exit:
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
        logo_rect = self.logo_image.get_rect(center=(app.width // 2, app.height // 5))
        screen.blit(self.logo_image, logo_rect)
        #title_text = self.title_font.render("Space Dodgers", True, (255, 255, 0))
        #title_rect = title_text.get_rect(center=(app.width // 2, app.height // 5))
        #screen.blit(title_text, title_rect)

        # High score below title
        if self.high_score > 0:
            hs_text = self.score_font.render(f"High Score: {self.high_score}", True, (255, 215, 0))
            hs_rect = hs_text.get_rect(center=(app.width // 2, app.height // 3 + 50))
            screen.blit(hs_text, hs_rect)

        # Menu nav
        menu_top = app.height // 3 + 50
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

        
