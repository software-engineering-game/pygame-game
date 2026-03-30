import pygame
import random
import os
import math
from states.base_state import State
from states import settings
from states import utils
from states.death_state import DeathState  #ADDED: death screen


# assets folder is at repo root
repo_root = os.path.dirname(os.path.dirname(__file__))
asset_folder = os.path.join(repo_root, "assets")


# Sprite is a base class from the Pygame Library
# def __init__(pygame, sprite, width, height, x, y):
# Class for the basic bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, asset_folder, sprite_name, speed, start_pos, direct):
        super().__init__()
        self.image = pygame.image.load(os.path.join(asset_folder, sprite_name)).convert()
        self.image.set_colorkey(utils.SHEET_BG)
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
    def __init__(self, frames, speed, start_pos):
        super().__init__()

        # Animation related variables
        self.frames = frames
        self.current_frame = 0
        self.last_update = 0
        self.animation_speed = 100  # milliseconds
        self.image = self.frames[self.current_frame]

        # Old functionality without animation, incase something breaks during testing
        # self.image = pygame.image.load(os.path.join(asset_folder, sprite_name)).convert()
        # self.image.set_colorkey(utils.SHEET_BG)
        self.rect = self.image.get_rect(center=start_pos)

        self.hitbox = self.rect.scale_by(0.3)
        self.hitbox.center = (self.rect.centerx, self.rect.centery)

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
        sfx_shoot = pygame.mixer.Sound("assets/sfx/shoot.wav")
        pygame.mixer.Sound.play(sfx_shoot)

    def update(self, keys):
        dx = dy = 0

        # Animation that loops the frames
        current_time = pygame.time.get_ticks()
        # If times since last frame update exceeds the millisecond interval
        if current_time - self.last_update > self.animation_speed:
            self.last_update = current_time
            # Sets it to current_frame + 1, unless it exceeds the total number of frames
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
        
        # Setting up WASD movement 
        keys = pygame.key.get_pressed()
        
        if keys[settings.keybind_player_left] or keys[pygame.K_a]:
            dx -= self.speed
        if keys[settings.keybind_player_right] or keys[pygame.K_d]:
            dx += self.speed
        if keys[settings.keybind_player_up] or keys[pygame.K_w]:
            dy -= self.speed
        if keys[settings.keybind_player_down] or keys[pygame.K_s]:
            dy += self.speed

        self.rect.x += dx
        self.rect.y += dy


class Basic_Enemy(pygame.sprite.Sprite):
    def __init__(self, frames, start_pos):
        super().__init__()

        self.frames = frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]

        self.vertical_speed = random.uniform(0.8, 1.5)
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = random.uniform(0.8, 1.5)

        # how often direction changes
        self.change_timer = random.uniform(1.0, 3.0)
        

        # self.image = pygame.image.load(os.path.join(asset_folder, sprite_name)).convert()
        # self.image.set_colorkey(utils.SHEET_BG)
        self.rect = self.image.get_rect(center=start_pos)
        self.speed = settings.basic_enemy_spd

        # Shooting cooldown tracking
        self.shoot_cooldown = random.uniform(2.5, 5.0)
        self.can_shoot = False

    def shoot(self, bullet_group):
        enemy_bullet = Bullet(
            asset_folder=asset_folder,
            sprite_name="basic_bullet.png",
            speed=settings.BULLET_SPEED,
            start_pos=(self.rect.centerx, self.rect.bottom),
            direct=(0, 1)
        )
        bullet_group.add(enemy_bullet)
        self.can_shoot = False
        self.shoot_cooldown = random.uniform(2.5, 5.0)

    def update(self, player_pos):
        # Move based on velocity
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Occasionally change direction (this is the key to "flow")
        self.change_timer -= 0.016  # approx frame time

        if self.change_timer <= 0:
            self.vx = random.uniform(-1.5, 1.5)
            self.vy = random.uniform(0.8, 1.5)
            self.change_timer = random.uniform(1.0, 3.0)
            self.vx = max(-2, min(2, self.vx))
            self.vy = max(0.5, min(2, self.vy))

        if self.rect.right < 0:
            self.rect.left = settings.WIDTH

        elif self.rect.left > settings.WIDTH:
            self.rect.right = 0

        # If enemy goes off bottom → reset to top
        if self.rect.top > settings.HEIGHT:
            self.rect.x = random.randint(50, settings.WIDTH - 50)
            self.rect.y = random.randint(-100, -40)

# Bomber enemy that releases an exploding payload
class Bomber_Enemy(pygame.sprite.Sprite):
    def __init__(self, asset_folder, sprite_name, start_pos):
        super().__init__()
        self.image = pygame.image.load(os.path.join(asset_folder, sprite_name)).convert()
        self.image.set_colorkey(utils.SHEET_BG)
        self.rect = self.image.get_rect(center=start_pos)
        self.speed = 0 # Placeholder

    def shoot(self, bullet_group):
        # For the bomber specific shooting mechanics
        pass

    def update(self, player_pos):
        # This where enemy movement goes, I was thinking a horizontal line
        pass

class Swarm_Enemy(pygame.sprite.Sprite):
    def __init__(self, asset_folder, sprite_name, start_pos):
        super().__init__()
        self.original_image = pygame.image.load(os.path.join(asset_folder, sprite_name)).convert()
        self.original_image.set_colorkey(utils.SHEET_BG)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=start_pos)
        self.speed = settings.swarm_enemy_spd

        self.velocity = (0,0)
        self.angle = 0

    def shoot(self, bullet_group):
        pass

    def update(self, player_pos):
        self.velocity = ((player_pos[0] - self.rect.x), (player_pos[1] - self.rect.y))

        distance = ((self.velocity[0] ** 2) + (self.velocity[1] ** 2)) ** 0.5
        if distance == 0:
            self.velocity = (0,0)
            dx = 0
            dy = 0
        else:
            dx = (self.velocity[0] / distance) * self.speed
            dy = (self.velocity[1] / distance) * self.speed

            # atan2 gives angle from positive x-axis; subtract 90 so "up" on the sprite faces the target
            import math
            self.angle = math.degrees(math.atan2(-self.velocity[1], self.velocity[0])) - 90

        center = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.image.set_colorkey(utils.SHEET_BG)
        self.rect = self.image.get_rect(center=center)

        self.rect.x += dx
        self.rect.y += dy

class GameState(State):
    saved_player_position = None

    def on_enter(self, app):
        self.app = app
        pygame.init()
        pygame.mixer.init(devicename="pygame.mixer.get_dev_info()")
        
        # Sets the background color, and draws the image
        self.bg_color = (0, 0, 0)
        #bg_name = "background_asteroids.png"
        #self.bg_image = pygame.image.load(os.path.join(asset_folder, bg_name))

        # Creates the sprite groups
        self.ally_ships = pygame.sprite.Group()
        self.ally_bullets = pygame.sprite.Group()
        self.enemy_ships = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()

        # Countdown for player readiness
        self.countdown = 3.0   # seconds
        self.countdown_active = True

        # Spawning Enemies
        self.enemy_ships.empty()

        num_enemies = 10
        columns = num_enemies

        spacing_x = app.width // columns

        for i in range(num_enemies):
            # base position in column
            x = i * spacing_x + spacing_x // 2

            # add small randomness so it's not perfectly aligned
            x += random.randint(-20, 20)

            # spawn in top 1/4
            y = random.randint(0, app.height // 4)

            enemy = Basic_Enemy(
                frames=utils.load_spritesheet(
                    asset_folder=asset_folder,
                    sheet_name="enemy_basic.png",
                    key_color=utils.SHEET_BG,
                    frame_width=utils.FRAME_SIZE,
                    frame_height=utils.FRAME_SIZE
                ),
                speed=2,
                start_pos=(x, y)
            )

            self.enemy_ships.add(enemy)



        # self.ram_ship = Swarm_Enemy(
        #     asset_folder=asset_folder,
        #     sprite_name="enemy_swarm.png",
        #     start_pos=(settings.WIDTH / 2, settings.HEIGHT / 2)
        # )
        # self.enemy_ships.add(self.ram_ship)

        # Spawning Player
        player_speed = 5
        self.player = Player(
            # Loads the sprite sheet into the player's frames
            frames=utils.load_spritesheet(
                asset_folder=asset_folder,
                sheet_name="player_shotgun_ship.png",
                key_color=utils.SHEET_BG,
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

        if self.countdown_active:
            self.countdown -= dt

            if self.countdown <= 0:
                self.countdown_active = False

            return

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

        if pygame.sprite.spritecollide(self.player, self.enemy_ships, False):
            app.change_state(DeathState("You Died", self.enemy_hit_count))
            return

        if pygame.sprite.spritecollide(self.player, self.enemy_bullets, False):
            sfx_player_boom = pygame.mixer.Sound("assets/sfx/p_boom.wav")
            pygame.mixer.Sound.play(sfx_player_boom)
            app.change_state(DeathState("You Died", self.enemy_hit_count))
            return
        
        if pygame.sprite.spritecollide(self.player, self.enemy_bullets, True):
            app.change_state(DeathState("You Died", self.enemy_hit_count))
            sfx_player_boom = pygame.mixer.Sound("assets/sfx/p_boom.wav")
            pygame.mixer.Sound.play(sfx_player_boom)
            return

        # ✅ ADDED: if enemy touches player -> go to death screen
        if pygame.sprite.spritecollide(self.player, self.enemy_ships, False):
            app.change_state(DeathState("You Died", self.enemy_hit_count))
            sfx_player_boom = pygame.mixer.Sound("assets/sfx/p_boom.wav")
            pygame.mixer.Sound.play(sfx_player_boom)
            return
        
        # If enemy bullet hits player -> go to death screen
        if pygame.sprite.spritecollide(self.player, self.enemy_bullets, True):
            app.change_state(DeathState("You Died", self.enemy_hit_count))
            sfx_player_boom = pygame.mixer.Sound("assets/sfx/p_boom.wav")
            pygame.mixer.Sound.play(sfx_player_boom)
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
            sfx_boom = pygame.mixer.Sound("assets/sfx/en_boom.wav")
            pygame.mixer.Sound.play(sfx_boom)
            self.enemy_hit_count += len(collisions)


    def draw(self, app, screen):
        screen.fill(self.bg_color)
        screen.blit(self.bg_image, (0, 0))
        self.ally_ships.draw(screen)
        self.enemy_ships.draw(screen)
        self.ally_bullets.draw(screen)
        self.enemy_bullets.draw(screen)


        if self.countdown_active:
            font = pygame.font.Font(None, 200)

            count = int(self.countdown) + 1  # makes it show 3,2,1

            if count > 0:
                text = font.render(str(count), True, (255, 255, 255))
            else:
                text = font.render("GO", True, (255, 255, 255))

            rect = text.get_rect(center=(app.width // 2, app.height // 2))
            screen.blit(text, rect)

        
        # delete after testing
        # pygame.draw.rect(screen, (255,255,255), self.player.hitbox)

        # Draw hit counter
        font = pygame.font.Font(None, 36)
        counter_text = font.render(f"Hits: {self.enemy_hit_count}", True, (255, 255, 255))
        screen.blit(counter_text, (10, 10))

