import pygame
import random
import math
import utils

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



class Swarm_Enemy():
    pass

