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

# Basic Grunt Enemy
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

# Not sure why this duplicate is here, but I assume it's for a more advanced enemy type
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

class GameState(State):
    def on_enter(self, app):
        self.app = app
        # assets folder is at repo root
        repo_root = os.path.dirname(os.path.dirname(__file__))
        asset_folder = os.path.join(repo_root, "assets")
        bg_name = "asteroid_background.png"

        self.bg_color = (0, 0, 0)
        self.bg_image = pygame.image.load(os.path.join(asset_folder, bg_name))

        self.ally_ships = pygame.sprite.Group()
        self.ally_bullets = pygame.sprite.Group()
        self.enemy_ships = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()

        self.spawn_basic_enemy_wave(
            asset_folder=asset_folder,
            sprite_name=settings.ENEMY_BASIC_SPRITE,
            speed=settings.ENEMY_SPD,
            corner_pos=(settings.WAVE_CORNER_X, settings.WAVE_CORNER_Y),
            rows=settings.WAVE_ROWS,
            columns=settings.WAVE_COLUMNS,
            spacing=(settings.WAVE_X_SPACING, settings.WAVE_Y_SPACING)
        )

        self.player = Player(
            asset_folder=asset_folder,
            sprite_name="player_shotgun_ship.png",
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
        screen.blit(self.bg_image, (0,0))
        self.ally_ships.draw(screen)
        self.enemy_ships.draw(screen)

    def spawn_basic_enemy_wave(self, asset_folder, sprite_name, speed, corner_pos, rows, columns, spacing):
        for j in range(rows):
            for i in range(columns):
                (x, y) = (corner_pos[0] + i * spacing[0], corner_pos[1] + j * spacing[1])
                enemy = Basic_Enemy(asset_folder, sprite_name, speed, (x, y))
                self.enemy_ships.add(enemy)
