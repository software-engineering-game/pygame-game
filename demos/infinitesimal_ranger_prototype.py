#something.py
# Coding Credits:
# Thomas Bond
#
#
#
#Date: 2026-02-05
import pygame
import os

#
# pygame setup
#

# Asset Folders
# We will need to update this section of the code as the projects directory structure changes
# because the os.path features are dependent on that structure
src_folder = os.path.dirname(__file__) # Establishes directory pointer for the files current directory
asset_folder = os.path.join(src_folder, "assets") # Looks for the directory 'assets' within the primary_game_folder and creates a directory pointer to it

# Global Variables
FRAMECAP = 60 # Number of ticks per second
DISPLAY_WIDTH = 720
DISPLAY_HEIGHT = 720
GAME_TITLE = "Infinitesimal Ranger" # Placeholder name until we decide on the style of the game
BLACK = (0,0,0)
BACKGROUND_COLOR = BLACK # Currently defines the background as solid color black

# Keybinds
# Sets the default keybinds
keybind_left = pygame.K_LEFT
keybind_right = pygame.K_RIGHT
keybind_up = pygame.K_UP
keybind_down = pygame.K_DOWN

#
# Entity Classes
#

# Player Variables
#PLAYER_WIDTH = 23 # Bounding box width
#PLAYER_HEIGHT = 30 # Bounding box height
PLAYER_SPRITE = "test_sprite.png" # Sets the name of the image to use for the player sprite
PLAYER_SPD = 5

# Defines Player Behavior
class Player(pygame.sprite.Sprite):
    def __init__(self): # Constructor (or initializer) for the player class
        pygame.sprite.Sprite.__init__(self) # Uses the pygame init function for sprites
        self.image = pygame.image.load(os.path.join(asset_folder, PLAYER_SPRITE)).convert() # Sets the path for the player sprite image
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect() # Sets the box that handles player hit detection and space
        # Currently bases the bounding box off the player sprite. THIS WILL NEED TO BE CHANGED
        # most games don't link the sprite to the hitbox directly because doing so just feels needlessly punishing
        # but for the purposes of setting this up that's what we'll use for now

        self.rect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT - 50) # Sets the initial location of the bounding box's center

        self.speedx = 0 # Sets initial x speed of player
        self.speedy = 0 # Sets initial y speed of player

    # Defines player object behavior
    def update(self):
        # Resets Speed
        self.speedx = 0
        self.speedy = 0

        # Checks which key is pressed and updates speed accordingly
        keystate = pygame.key.get_pressed()

        if keystate[keybind_left]: # Move left
            self.speedx = PLAYER_SPD * -1
        if keystate[keybind_right]: # Move right
            self.speedx = PLAYER_SPD
        if keystate[keybind_left] and keystate[keybind_right]: # Don't move
            self.speedx = 0

        if keystate[keybind_up]: # Move up
            self.speedy = PLAYER_SPD * -1
        if keystate[keybind_down]: # Move down
            self.speedy = PLAYER_SPD
        if keystate[keybind_up] and keystate[keybind_down]: # Don't move
            self.speedy = 0

        # Updates position
        self.rect.x += self.speedx
        self.rect.y += self.speedy

# Enemy Variables
#ENEMY_WIDTH = 23 # Bounding box width
#ENEMY_HEIGHT = 30 # Bounding box height
ENEMY_SPRITE = "cat.png" # Sets the name of the image to use for the enemy sprite
ENEMY_SPD = 0

# Defines Basic Enemy Behavior
class Enemy(pygame.sprite.Sprite):
    def __init__(self): # Constructor (or initializer) for the player class
        pygame.sprite.Sprite.__init__(self) # Uses the pygame init function for sprites
        self.image = pygame.image.load(os.path.join(asset_folder, ENEMY_SPRITE)).convert() # Sets the path for the player sprite image
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect() # Sets the box that handles player hit detection and space
        # Currently bases the bounding box off the player sprite. THIS WILL NEED TO BE CHANGED
        # most games don't link the sprite to the hitbox directly because doing so just feels needlessly punishing
        # but for the purposes of setting this up that's what we'll use for now

        self.rect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2) # Sets the initial location of the bounding box's center

        self.speedx = 0 # Sets initial x speed of player
        self.speedy = 0 # Sets initial y speed of player

    # Defines player object behavior
    def update(self):
        # Resets Speed
        self.speedx = 0
        self.speedy = 0

        # the update function can't handle animations it just updates the object variables

# Initialize Pygame
pygame.init()
#pygame.mixer.init() # Initializes the audio
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT)) # Initializes the screen display
pygame.display.set_caption(GAME_TITLE) # Names the Window the game runs in
clock = pygame.time.Clock()

#
# Game Loop
#

# Entities
ally_sprites = pygame.sprite.Group() # Creates a group for ally sprites, player and pellets
player = Player() # Declares a player object
ally_sprites.add(player) # Adds the player to the group of ally_sprites

enemy_sprites = pygame.sprite.Group() # Creates a group for enemy sprites, enemies and their pellets
enemy1 = Enemy() # Declares an enemy object
enemy_sprites.add(enemy1) # Adds the enemy1 to the group of enemy_sprites

running = True # Condition used to indicate the game is running
while running:
    #
    # Process Events and Input
    #

    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # pygame.QUIT event means the user clicked X to close your window
            running = False

    #
    # Update Game State
    #

    ally_sprites.update()
    enemy_sprites.update()

    #
    # Render Game
    #

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BACKGROUND_COLOR)

    ally_sprites.draw(screen) # Draws all sprites to the screen
    enemy_sprites.draw(screen)

    # Displays the draw calls for this frame
    # ALWAYS DO THIS AFTER DRAW CALLS that you want displayed on a given frame
    pygame.display.flip()

    clock.tick(FRAMECAP)  # Sets FPS limit

pygame.quit()