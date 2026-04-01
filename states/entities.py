import pygame
import random
import math
from states.utils import load_spritesheet
from states import settings

# Class for menu star effect
class Stars:
    def __init__(self, w, h):
        self.x = random.randint(0, w - 1)
        self.y = random.randint(0, h - 1)
        self.r = random.choice([1, 1, 1, 2])
        self.base = random.randint(100, 180)
        self.amp = random.randint(20, 80)
        self.speed = random.uniform(1.0, 4.0)
        self.phase = random.uniform(0, math.tau)

    def brightness(self, t):
        b = self.base + self.amp * math.sin(t * self.speed + self.phase)
        return max(0, min(255, int(b)))
    
    def draw(self, screen, t):
        b = self.brightness(t)
        pygame.draw.circle(screen, (b, b, b), (self.x, self.y), self.r)

#
# Classes for Game Entities
#

# Sprite is a base class from the Pygame Library
# def __init__(pygame, sprite, width, height, x, y):

class Game_Entity(pygame.sprite.Sprite):
    def __init__(self, frames, speed, start_pos):
        super().__init__()

        # Animation related variables
        self.frames = frames
        self.current_frame = 0
        self.last_update = 0
        self.animation_speed = 100  # milliseconds
        self.image = self.frames[self.current_frame]

        # Bounding Box
        self.rect = self.image.get_rect(center=start_pos)
        # Hitbox
        self.hitbox = self.rect.scale_by(1)

        self.speed = speed
    
    def update(self):
        pass

class Bullet(Game_Entity):
    def __init__(self, frames, speed, start_pos, direct):
        super().__init__(frames, speed, start_pos)

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

#
# Player Ship Types
#

# Base Class for standard player ship
class Player(Game_Entity):
    def __init__(self, frames, speed, start_pos):
        super().__init__(frames, speed, start_pos)

        # Hitbox
        self.hitbox = self.rect.scale_by(0.3)
        self.hitbox.center = (self.rect.centerx, self.rect.centery)

        # Shooting cooldown tracking
        self.shoot_cooldown = 0.0
        self.can_shoot = True

    def shoot(self, bullet_group):
        pass

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
        self.hitbox.x += dx
        self.rect.y += dy
        self.hitbox.y += dy

# Class for the standard firing mode
class Player_Auto(Player):
    def __init__(self, frames, speed, start_pos):
        super().__init__(frames, speed, start_pos)
    
    def shoot(self, bullet_group):
        # Spawns the bullet and adds it to bullet group
        player_bullet = Bullet(
            frames=load_spritesheet(
                sheet_name="basic_bullet.png",
                frame_width=10,
                frame_height=16
            ),
            speed=settings.BULLET_SPEED,
            start_pos=(self.rect.centerx, self.rect.top),
            direct=(0, -1)
        )
        bullet_group.add(player_bullet)
        self.can_shoot = False
        self.shoot_cooldown = settings.BULLET_COOLDOWN

#
class Player_Shotgun(Player):
    def __init__(self, frames, speed, start_pos):
        super().__init__(frames, speed, start_pos)

#
class Player_Sniper(Player):
    def __init__(self, frames, speed, start_pos):
        super().__init__(frames, speed, start_pos)

#
# Enemy Ship Types
#

# Basic Enemy type
class Basic_Enemy(Game_Entity):
    def __init__(self, frames, start_pos):
        super().__init__(frames, speed=settings.basic_enemy_spd, start_pos=start_pos)

        # Hitbox
        self.hitbox = self.rect.scale_by(0.4)

        self.vertical_speed = random.uniform(0.8, 1.5)
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = random.uniform(0.8, 1.5)

        # how often direction changes
        self.change_timer = random.uniform(1.0, 3.0)
        


        # Shooting cooldown tracking
        self.shoot_cooldown = random.uniform(1.0, 5.0)
        self.can_shoot = False

    def shoot(self, bullet_group):
        enemy_bullet = Bullet(
            frames=load_spritesheet(
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
        self.shoot_cooldown = random.uniform(2.0, 5.0)

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

# Swarm Enemy Type
class Swarm_Enemy(Game_Entity):
    def __init__(self, frames, start_pos):
        super().__init__(frames, speed=settings.swarm_enemy_spd, start_pos=start_pos)
        self.original_image = self.image

        # Hitbox
        self.hitbox = self.rect.scale_by(0.4)

        # Player Tracking Variables
        self.velocity = (0,0)
        self.angle = 0

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
        self.rect = self.image.get_rect(center=center)

        self.rect.x += dx
        self.rect.y += dy

# Bomber Enemy Type
class Bomber_Enemy(Game_Entity):
    def __init__(self, frames, start_pos):
        super().__init__(frames, speed=settings.bomber_enemy_spd, start_pos=start_pos)

        # Hitbox
        self.hitbox = self.rect.scale_by(0.4)

    def shoot(self, bullet_group):
        # for when I write the bomber specific mechanics
        pass
    
    def update(self, player_pos):
        # Enemy behavior
        pass
