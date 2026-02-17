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

    def change_state(self, new_state):
        if self.state is not None:
            self.state.on_exit(self)
        self.state = new_state
        self.state.on_enter(self)

async def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption(settings.TITLE)

    app = App(screen)
    app.change_state(MainMenuState())

    clock = pygame.time.Clock()

    while app.running:
        dt = clock.tick(FPS) / 1000.0

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
