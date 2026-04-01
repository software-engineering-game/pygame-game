import pygame
import random
import os
from states import settings
from states import utils
from states.base_state import State
from states.death_state import DeathState  #ADDED: death screen
from states import entities

# assets folder is at repo root
repo_root = os.path.dirname(os.path.dirname(__file__))
asset_folder = os.path.join(repo_root, "assets")

class Basic_Enemy(pygame.sprite.Sprite):
    def __init__(self, frames, start_pos):
        super().__init__()

        self.frames = frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]

        # Bounding Box
        self.rect = self.image.get_rect(center=start_pos)
        self.speed = settings.basic_enemy_spd

        # Shooting cooldown tracking
        self.shoot_cooldown = random.uniform(1.0, 3.0)
        self.can_shoot = False

    def shoot(self, bullet_group):
        enemy_bullet = entities.Bullet(
            frames=utils.load_spritesheet(
                sheet_name="basic_bullet.png",
                frame_width=10,
                frame_height=16
            ),
            speed=settings.BULLET_SPEED,
            start_pos=(self.rect.centerx, self.rect.bottom),
            direct=(0, 1)
        )
        bullet_group.add(enemy_bullet)
        self.can_shoot = False
        self.shoot_cooldown = random.uniform(3.0, 8.0)

    def update(self, player_pos):
        # this is where basic enemy movement should go
        pass

class GameState(State):
    saved_player_position = None

    def on_enter(self, app):
        self.app = app
        
        # Sets the background color, and draws the image
        self.bg_color = (0, 0, 0)
        #bg_name = "background_asteroids.png"
        #self.bg_image = pygame.image.load(os.path.join(asset_folder, bg_name))

        # Creates the sprite groups
        self.ally_ships = pygame.sprite.Group()
        self.ally_bullets = pygame.sprite.Group()
        self.enemy_ships = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()

        # Building Level
        self.bg_image = utils.build_level(
            level_name="first_level",
            enemy_ships=self.enemy_ships,
            temp_type=entities.Basic_Enemy
        )

        # Spawning Player
        player_speed = 5
        self.player = entities.Player_Auto(
            # Loads the sprite sheet into the player's frames
            frames=utils.load_spritesheet(
                sheet_name="player_auto_ship.png",
                frame_width=utils.FRAME_SIZE,
                frame_height=utils.FRAME_SIZE
            ),
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

        # Enemy auto-fire logic for basic enemies
        for enemy in self.enemy_ships:
            if isinstance(enemy, Basic_Enemy):
                enemy.shoot_cooldown -= dt
                if enemy.shoot_cooldown <= 0 and not enemy.can_shoot:
                    enemy.can_shoot = True

                if enemy.can_shoot:
                    enemy.shoot(self.enemy_bullets)

        # ✅ ADDED: if enemy touches player -> go to death screen
        if pygame.sprite.spritecollide(self.player, self.enemy_ships, False):
            app.change_state(DeathState("You Died", self.enemy_hit_count))
            return
        
        # If enemy bullet hits player -> go to death screen
        if pygame.sprite.spritecollide(self.player, self.enemy_bullets, True):
            app.change_state(DeathState("You Died", self.enemy_hit_count))
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
        self.enemy_bullets.update()
        
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
        self.enemy_bullets.draw(screen)
        
        # delete after testing
        # pygame.draw.rect(screen, (255,255,255), self.player.hitbox)

        # Draw hit counter
        font = pygame.font.Font(None, 36)
        counter_text = font.render(f"Hits: {self.enemy_hit_count}", True, (255, 255, 255))
        screen.blit(counter_text, (10, 10))

