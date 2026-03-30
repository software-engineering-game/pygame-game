import pygame
import asyncio
from states.main_menu_state import MainMenuState
from states import settings

class App:
    def __init__(self, screen):
        self.screen = screen
        self.width = settings.WIDTH
        self.height = settings.HEIGHT
        self.running = True
        self.state = None
        self.music_playing = False

    def change_state(self, new_state):
        if self.state is not None:
            self.state.on_exit(self)
        self.state = new_state
        self.state.on_enter(self)
    
    def play_music(self, track="assets/audio/music/main_theme.ogg"):
        if not self.music_playing:
            pygame.mixer.music.load(track)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            self.music_playing = True
    
    def stop_music(self):
        pygame.mixer.music.fadeout(500)
        self.music_playing = False

async def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption(settings.TITLE)

    app = App(screen)
    app.change_state(MainMenuState())

    clock = pygame.time.Clock()

    while app.running:
        dt = clock.tick(settings.FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app.running = False
            else:
                app.state.handle_event(app, event)

        app.state.update(app, dt)
        app.state.draw(app, screen)

        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())
