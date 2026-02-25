#something.py
# Coding Credits:
# Thomas Bond
#
#
#
#Date: 2026-02-05
import asyncio
import pygame
import os

#
# pygame setup
#
# Constants
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


WINDOW_SIZE = (1280, 720)
WINDOW_TITLE = "Infinitesimal Ranger"


BOUNDS_X = (66, 1214)
BOUNDS_Y = (50, 620)


HORIZONTAL = 1
UP = 2
DOWN = 0


FRAME_RATE = 60
ANIMATION_FRAME_RATE = 10


WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(WINDOW_TITLE)


CLOCK = pygame.time.Clock()
# Asset Folders
# We will need to update this section of the code as the projects directory structure changes
# because the os.path features are dependent on that structure
primary_game_folder = os.path.dirname(__file__) # Establishes directory pointer for the files current directory
img_folder = os.path.join(primary_game_folder, "assets") # Looks for the directory 'assets' within the primary_game_folder and creates a directory pointer to it




objects = []
bullets = []
enemies = []




# Global Variables
FRAMECAP = 60 # Number of ticks per second
DISPLAY_HEIGHT = 720
DISPLAY_WIDTH = 1280
# Placeholder name until we decide on the style of the game
BACKGROUND_COLOR = BLACK # Currently defines the background as solid color black


# Player Variables
#PLAYER_WIDTH = 23 # Bounding box width
#PLAYER_HEIGHT = 30 # Bounding box height
PLAYER_SPRITE = "test_sprite.png" # Sets the name of the image to use for the player sprite
PLAYER_SPD = 5


# Keybinds
# Sets the default keybinds
keybind_left = pygame.K_LEFT
keybind_right = pygame.K_RIGHT
keybind_up = pygame.K_UP
keybind_down = pygame.K_DOWN


#
# Entity Classes
#
class Object:
   def __init__(self, x, y, width, height, image):
       self.x = x
       self.y = y
       self.width = width
       self.height = height
       self.image = image
       self.velocity = [0, 0]
       self.collider = [width, height]


       objects.append(self)


   def draw(self):
       WINDOW.blit(pygame.transform.scale(self.image, (self.width, self.height)), (self.x, self.y))


   def update(self):
       self.x += self.velocity[0]
       self.y += self.velocity[1]
       self.draw()


   def get_center(self):
       return self.x + self.width / 2, self.y + self.height / 2


# Deals with
class Entity(Object):
   def __init__(self, x, y, width, height, tileset, speed):
       super().__init__(x, y, width, height, None)
       self.speed = speed


       self.tileset = load_tileset(tileset, 16, 16)
       self.direction = 0
       self.flipX = False
       self.frame = 0
       self.frames = [0, 1, 0, 2]
       self.frame_timer = 0


   def change_direction(self):
       if self.velocity[0] < 0:
           self.direction = HORIZONTAL
           self.flipX = True
       elif self.velocity[0] > 0:
           self.direction = HORIZONTAL
           self.flipX = False
       elif self.velocity[1] > 0:
           self.direction = DOWN
       elif self.velocity[1] < 0:
           self.direction = UP


   def draw(self):
       image = pygame.transform.scale(self.tileset[self.frames[self.frame]][self.direction],
                                      (self.width, self.height))


       self.change_direction()


       image = pygame.transform.flip(image, self.flipX, False)
       WINDOW.blit(image, (self.x, self.y))


       if self.velocity[0] == 0 and self.velocity[1] == 0:
           self.frame = 0
           return


       self.frame_timer += 1


       if self.frame_timer < ANIMATION_FRAME_RATE:
           return


       self.frame += 1
       if self.frame >= len(self.frames):
           self.frame = 0


       self.frame_timer = 0


   def update(self):
       self.x += self.velocity[0] * self.speed
       self.y += self.velocity[1] * self.speed
       self.draw()


pygame.mouse.set_visible(False)


      


class Enemy(Entity):
   def __init__(self, x, y, width, height, tileset, speed):
       super().__init__(x, y, width, height, tileset, speed)


       enemy_image = load_image(tileset, fallback_size=(16, 16), fallback_color=(255, 80, 80, 255))
       self.tileset = create_repeated_tileset_from_image(enemy_image, 16, 16)


       self.health = 3
       self.collider = [width / 2.5, height / 1.5]
       enemies.append(self)


   def update(self):
       player_center = player.get_center()
       enemy_center = self.get_center()


       self.velocity = [player_center[0] - enemy_center[0], player_center[1] - enemy_center[1]]


       magnitude = (self.velocity[0] ** 2 + self.velocity[1] ** 2) ** 0.5
       if magnitude == 0:
           self.velocity = [0, 0]
           super().update()
           return
       self.velocity = [self.velocity[0] / magnitude * self.speed, self.velocity[1] / magnitude * self.speed]


       super().update()


   def change_direction(self):
       super().change_direction()


       if self.velocity[1] > self.velocity[0] > 0:
           self.direction = DOWN
       elif self.velocity[1] < self.velocity[0] < 0:
           self.direction = UP


   def take_damage(self, damage):
       self.health -= damage
       if self.health <= 0:
           self.destroy()


   def destroy(self):
       objects.remove(self)
       enemies.remove(self)




def check_input(key, value):
   if key == pygame.K_LEFT or key == pygame.K_a:
       player_input["left"] = value
   elif key == pygame.K_RIGHT or key == pygame.K_d:
       player_input["right"] = value
   elif key == pygame.K_UP or key == pygame.K_w:
       player_input["up"] = value
   elif key == pygame.K_DOWN or key == pygame.K_s:
       player_input["down"] = value




def resolve_asset_path(filename):
   if os.path.isabs(filename):
       return filename
   return os.path.join(primary_game_folder, filename)




def create_placeholder_tileset(tile_width, tile_height, columns=3, rows=3):
   tileset = []
   for tile_x in range(columns):
       line = []
       tileset.append(line)
       for tile_y in range(rows):
           tile = pygame.Surface((tile_width, tile_height), pygame.SRCALPHA)
           tile.fill((80 + tile_x * 40, 80 + tile_y * 40, 180, 255))
           line.append(tile)
   return tileset




def create_repeated_tileset_from_image(image, tile_width, tile_height, columns=3, rows=3):
   tile = pygame.transform.scale(image, (tile_width, tile_height))
   tileset = []
   for _ in range(columns):
       line = []
       tileset.append(line)
       for _ in range(rows):
           line.append(tile.copy())
   return tileset




def load_image(filename, fallback_size=(16, 16), fallback_color=(255, 255, 255, 255)):
   resolved_filename = resolve_asset_path(filename)
   if os.path.exists(resolved_filename):
       return pygame.image.load(resolved_filename).convert_alpha()


   fallback = pygame.Surface(fallback_size, pygame.SRCALPHA)
   fallback.fill(fallback_color)
   return fallback




def load_tileset(filename, width, height):
   resolved_filename = resolve_asset_path(filename)
   if not os.path.exists(resolved_filename):
       return create_placeholder_tileset(width, height)


   image = pygame.image.load(resolved_filename).convert_alpha()
   image_width, image_height = image.get_size()


   if image_width < width * 3 or image_height < height * 3:
       return create_repeated_tileset_from_image(image, width, height)


   tileset = []
   for tile_x in range(0, image_width // width):
       line = []
       tileset.append(line)
       for tile_y in range(0, image_height // height):
           rect = (tile_x * width, tile_y * height, width, height)
           line.append(image.subsurface(rect))
   return tileset




player_input = {"left": False, "right": False, "up": False, "down": False}




pygame.mouse.set_visible(False)
   




  




# Defines Player Behavior
class Player(pygame.sprite.Sprite):
   def __init__(self): # Constructor (or initializer) for the player class
       pygame.sprite.Sprite.__init__(self) # Uses the pygame init function for sprites
       self.image = pygame.image.load(os.path.join(img_folder, PLAYER_SPRITE)).convert() # Sets the path for the player sprite image