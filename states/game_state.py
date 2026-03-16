import pygame
import os
from states.base_state import State
from states import settings
from states.death_state import DeathState  #ADDED: death screen

# This exists to key out spritesheet backgrounds
SHEET_BG = (160, 200, 152)

# assets folder is at repo root
repo_root = os.path.dirname(os.path.dirname(__file__))
asset_folder = os.path.join(repo_root, "assets")

# Class for the basic bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, asset_folder, sprite_name, speed, start_pos, direct):
        super().__init__()
        # Creates a simple laser bullet
        # self.image = pygame.Surface((4, 12))
        self.image = pygame.image.load(os.path.join(asset_folder, sprite_name)).convert()
        self.image.set_colorkey(SHEET_BG)
        self.rect = self.image.get_rect(center=start_pos)
        self.speed = speed

        self.x_direct = direct[0] # Should be set to 0, 1, or -1
        self.y_direct = direct[1] # Should be set to 0, 1, or -1
    
    def update(self):
        self.rect.x += self.x_direct * self.speed
        self.rect.y += self.y_direct * self.speed
        # Remove bullet if it goes off screen
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top > 740:
            self.kill()

# Class for standard player ship
class Player(pygame.sprite.Sprite):
    def __init__(self, asset_folder, sprite_name, speed, start_pos):
        super().__init__()
        self.image = pygame.image.load(os.path.join(asset_folder, sprite_name)).convert()
        self.image.set_colorkey(SHEET_BG)
        self.rect = self.image.get_rect(center=start_pos)
        self.rect.scale_by(0.2)
        self.speed = speed

        # Shooting cooldown tracking
        self.shoot_cooldown = 0.0
        self.can_shoot = True

    def shoot(self, bullet_group):
        player_bullet = Bullet(
            asset_folder=asset_folder,
            sprite_name="basic_bullet.png",
            speed=settings.BULLET_SPEED,
            start_pos=(self.rect.centerx, self.rect.top),
            direct=(0, -1)
        )
        bullet_group.add(player_bullet)
        self.can_shoot = False
        self.shoot_cooldown = settings.BULLET_COOLDOWN

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
        self.image.set_colorkey(SHEET_BG)
        self.rect = self.image.get_rect(center=start_pos)
        self.rect.scale_by(1)
        self.speed = speed

        # Shooting cooldown tracking
        self.shoot_cooldown = 0.0
        self.can_shoot = True

    def shoot(self, bullet_group):
        # for the basic enemy shooting mechanics
        pass

    def update(self, player_pos):
        # this is where basic enemy movement should go
        pass

# Bomber enemy that releases an exploding payload
class Bomber_Enemy(pygame.sprite.Sprite):
    def __init__(self, asset_folder, sprite_name, speed, start_pos):
        super().__init__()
        self.image = pygame.image.load(os.path.join(asset_folder, sprite_name)).convert()
        self.image.set_colorkey(SHEET_BG)
        self.rect = self.image.get_rect(center=start_pos)
        self.rect.scale_by(1)
        self.speed = speed

    def shoot(self, bullet_group):
        # For the bomber specific shooting mechanics
        pass

    def update(self, player_pos):
        # This where enemy movement goes, I was thinking a horizontal line
        pass

class Swarm_Enemy(pygame.sprite.Sprite):
    def __init__(self, asset_folder, sprite_name, speed, start_pos):
        super().__init__()
        self.image = pygame.image.load(os.path.join(asset_folder, sprite_name)).convert()
        self.image.set_colorkey(SHEET_BG)
        self.rect = self.image.get_rect(center=start_pos)
        #self.rect.scale_by(1)
        self.speed = speed

        self.velocity = (0,0) # Used for calculating direction to player

    def shoot(self, bullet_group):
        pass

    def update(self, player_pos):
        self.velocity = ((player_pos[0] - self.rect.x), (player_pos[1] - self.rect.y))

        # Distance equation
        distance = ((self.velocity[0] ** 2) + (self.velocity[1] ** 2)) ** 0.5
        if distance == 0:
            self.velocity = (0,0)
            dx = 0
            dy = 0
        else:
            dx = (self.velocity[0] / distance) * self.speed
            dy = (self.velocity[1] / distance) * self.speed
        
        self.rect.x += dx
        self.rect.y += dy
        #will need sprite rotations at some point

class GameState(State):
    saved_player_position = None

    def on_enter(self, app):
        self.app = app
        
        # Sets the background color, and draws the image
        bg_name = "asteroid_background.png"
        self.bg_color = (0, 0, 0)
        self.bg_image = pygame.image.load(os.path.join(asset_folder, bg_name))

        # Creates the sprite groups
        self.ally_ships = pygame.sprite.Group()
        self.ally_bullets = pygame.sprite.Group()
        self.enemy_ships = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()

        # Spawning Enemies
        enemy_sprite = "enemy_basic.png"
        self.spawn_basic_enemy_wave(
            asset_folder=asset_folder,
            sprite_name=enemy_sprite,
            speed=settings.ENEMY_SPD,
            corner_pos=(settings.WAVE_CORNER_X, settings.WAVE_CORNER_Y),
            rows=settings.WAVE_ROWS,
            columns=settings.WAVE_COLUMNS,
            spacing=(settings.WAVE_X_SPACING, settings.WAVE_Y_SPACING),
        )

        self.ram_ship = Swarm_Enemy(
            asset_folder=asset_folder,
            sprite_name="enemy_swarm.png",
            speed=3,
            start_pos=(settings.WIDTH / 2, settings.HEIGHT / 2)
        )
        self.enemy_ships.add(self.ram_ship)

        # Spawning Player
        player_speed = 5
        self.player = Player(
            asset_folder=asset_folder,
            sprite_name="player_shotgun_ship.png",
            speed=player_speed,
            start_pos=(app.width // 2, app.height - 50),
        )
        self.ally_ships.add(self.player)
        self.enemy_hit_count = 0

        # Restore saved position if returning from pause
        if GameState.saved_player_position is not None:
            self.player.rect.center = GameState.saved_player_position

    def handle_event(self, app, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # Save player position before pausing
            GameState.saved_player_position = self.player.rect.center
            from states.pause_state import PauseScreen
            app.change_state(PauseScreen(app, self))
        
        # Shooting input
        if event.type == pygame.KEYDOWN and event.key == settings.keybind_player_shoot:
            if self.player.can_shoot:
                self.player.shoot(self.ally_bullets)
    
    def update(self, app, dt):
        keys = pygame.key.get_pressed()
        self.player.update(keys)

        play_area = pygame.Rect(0, 0, app.width, app.height)
        self.player.rect.clamp_ip(play_area)

        player_pos = (self.player.rect.x, self.player.rect.y)
        self.enemy_ships.update(player_pos=player_pos)
                # ✅ ADDED: if enemy touches player -> go to death screen
        if pygame.sprite.spritecollide(self.player, self.enemy_ships, False):
            app.change_state(DeathState("You Died"))
            return

        # Update shooting cooldown
        if not self.player.can_shoot:
            self.player.shoot_cooldown -= dt
            if self.player.shoot_cooldown <= 0:
                self.player.can_shoot = True
        
        # Allow continuous shooting by holding spacebar
        if keys[settings.keybind_player_shoot] and self.player.can_shoot:
            self.player.shoot(self.ally_bullets)
        
        # Update bullets
        self.ally_bullets.update()
        
        # see if bullet hit an enemy
        collisions = pygame.sprite.groupcollide(
            self.ally_bullets, 
            self.enemy_ships, 
            True,  # Remove bullet on collision
            True   # Remove enemy on collision
        )
        #Score tracking for hits,
        if collisions:
            self.enemy_hit_count += len(collisions)

    def draw(self, app, screen):
        screen.fill(self.bg_color)
        screen.blit(self.bg_image, (0, 0))
        self.ally_ships.draw(screen)
        self.enemy_ships.draw(screen)
        self.ally_bullets.draw(screen)
        
        # Draw hit counter
        font = pygame.font.Font(None, 36)
        counter_text = font.render(f"Hits: {self.enemy_hit_count}", True, (255, 255, 255))
        screen.blit(counter_text, (10, 10))

    def spawn_basic_enemy_wave(
        self, asset_folder, sprite_name, speed, corner_pos, rows, columns, spacing
    ):
        for j in range(rows):
            for i in range(columns):
                (x, y) = (
                    corner_pos[0] + i * spacing[0],
                    corner_pos[1] + j * spacing[1],
                )
                enemy = Basic_Enemy(asset_folder, sprite_name, speed, (x, y))
                self.enemy_ships.add(enemy)