import pygame
import os
from states.base_state import State

BLACK = (0, 0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self, img_folder, sprite_name, speed, start_pos):
        super().__init__()
        self.image = pygame.image.load(os.path.join(img_folder, sprite_name)).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=start_pos)
        self.speed = speed

    def update(self, keys):
        dx = dy = 0
        if keys[pygame.K_LEFT]:  dx -= self.speed
        if keys[pygame.K_RIGHT]: dx += self.speed
        if keys[pygame.K_UP]:    dy -= self.speed
        if keys[pygame.K_DOWN]:  dy += self.speed
        self.rect.x += dx
        self.rect.y += dy


class GameState(State):
    def on_enter(self, app):
        self.bg = (0, 0, 0)

        # asset path (team can standardize)
        base = os.path.dirname(__file__)
        self.img_folder = os.path.join(os.path.dirname(base), "assets")

        self.allies = pygame.sprite.Group()

        self.player = Player(
            img_folder=self.img_folder,
            sprite_name="test_sprite.png",
            speed=5,
            start_pos=(app.width // 2, app.height - 50),
        )
        self.allies.add(self.player)

    def handle_event(self, app, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            from states.main_menu_state import MainMenuState
            app.change_state(MainMenuState())

    def update(self, app, dt):
        keys = pygame.key.get_pressed()
        self.player.update(keys)

    def draw(self, app, screen):
        screen.fill(self.bg)
        self.allies.draw(screen)
