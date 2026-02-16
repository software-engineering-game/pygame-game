import pygame
import asyncio

WIDTH, HEIGHT = 720, 720
TITLE = "Space Dodgers"
FPS = 60

class State:
    def handle_event(self, event):
        pass
    def update(self, dt):
        pass
    def draw(self, screen):
        pass

async def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        pygame.display.flip()

        await asyncio.sleep(0) # this is for pygbag

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
