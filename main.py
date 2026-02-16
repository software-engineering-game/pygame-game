import pygame
import asyncio
from states.menu_state import MainMenuState

WIDTH, HEIGHT = 720, 720
TITLE = "Space Dodgers"
FPS = 60

class App:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.state = None
    
    def change_state(self, new_state):
        if self.state is not None:
            self.state.on_exit(self)

        self.state = new_state
        self.state.on_enter(self)


async def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    app = App(screen)
    app.change_state(MainMenuState())

    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()
    state = MainMenuState()
    running = True

    while app.running:
        dt = clock.tick(FPS) / 1000.0  # seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                state.handle_event(app, event)

        app.state.update(app, dt)
        app.state.draw(app, screen)

        pygame.display.flip()
        await asyncio.sleep(0) # this is for pygbag

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
