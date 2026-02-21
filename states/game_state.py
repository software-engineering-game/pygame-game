import pygame
import os
from states.base_state import State
from states import settings
BLACK = (0, 0, 0) # This exists solely to key out the transparency for sprites

class Player(pygame.sprite.Sprite):
    def __init__(self, asset_folder, sprite_name, speed, start_pos):
        super().__init__()
        self.image = pygame.image.load(os.path.join(asset_folder, sprite_name)).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=start_pos) # I still want to find a way to change the bounding box
        self.speed = speed

    def update(self, keys):
        dx = dy = 0

        if keys[settings.keybind_player_left]:
            dx -= self.speed
        if keys[settings.keybind_player_right]:
            dx += self.speed
        if keys[settings.keybind_player_up]:
            dy -= self.speed
        if keys[settings.keybind_player_down]:
            dy += self.speed

        self.rect.x += dx
        self.rect.y += dy

class Basic_Enemy(pygame.sprite.Sprite):
    def __init__(self, asset_folder, sprite_name, speed, start_pos):
        super().__init__()
        self.image = pygame.image.load(os.path.join(asset_folder, sprite_name)).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=start_pos)
        self.speed = speed

    def update(self):
        # This is where basic enemy behavior should go
        pass

class GameState(State):
    def on_enter(self, app):
        self.app = app
        # assets folder is at repo root
        repo_root = os.path.dirname(os.path.dirname(__file__))
        asset_folder = os.path.join(repo_root, "assets")

        self.bg_color = (0, 0, 0)

        self.ally_ships = pygame.sprite.Group()
        self.ally_bullets = pygame.sprite.Group()
        self.enemy_ships = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()

        self.spawn_basic_enemy_wave(asset_folder)

        self.player = Player(
            asset_folder=asset_folder,
            sprite_name="test_sprite.png",
            speed=5,
            start_pos=(app.width // 2, app.height - 50),
        )
        self.ally_ships.add(self.player)

    def handle_event(self, app, event):
        # To get to pause screen
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            from states.pause_state import PauseScreen
            app.change_state(PauseScreen(app, self))

    def update(self, app, dt):
        keys = pygame.key.get_pressed()
        self.player.update(keys)
        self.enemy_ships.update()

    def draw(self, app, screen):
        screen.fill(self.bg_color)
        self.ally_ships.draw(screen)
        self.enemy_ships.draw(screen)

    def spawn_basic_enemy_wave(self, asset_folder):
        for j in range(settings.WAVE_ROWS):
            for i in range(settings.WAVE_COLUMNS):
                x = settings.WAVE_CORNER_X + i * settings.WAVE_X_SPACING
                y = settings.WAVE_CORNER_Y + j * settings.WAVE_Y_SPACING
                enemy = Enemy(asset_folder, settings.ENEMY_BASIC_SPRITE, settings.ENEMY_SPD, (x, y))
                self.enemy_ships.add(enemy)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, asset_folder, sprite_name, speed, start_pos):
        super().__init__()
        self.image = pygame.image.load(os.path.join(asset_folder, sprite_name)).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=start_pos)
        self.speed = speed

    def update(self):
        # need to add movement and shooting later
        pass
