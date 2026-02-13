# This is the main file where all the code for the game will go. 

import pygame
import os
import asyncio

# Asset Folders
# we will need to update this section of the code as the projects directory structure changes
# because the os.path features are dependent on that structure
primary_game_folder = os.path.dirname(__file__)  # Establishes directory pointer for the files current directory
img_folder = os.path.join(primary_game_folder, "assets")  # Looks for the directory 'assets' within the primary_game_folder and creates a directory pointer to it

# Global Variables
FRAMECAP = 60  # Number of ticks per second
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720
GAME_TITLE = "Placeholder"  
BLACK = (0, 0, 0)
BACKGROUND_COLOR = BLACK  # Currently defines the background as solid color black


# PLAYER_WIDTH = 23 
# PLAYER_HEIGHT = 30 
PLAYER_SPRITE = "test_sprite.png"  # Sets the name of the image to use for the player sprite
PLAYER_SPD = 5

# default keybinds
keybind_left = pygame.K_LEFT
keybind_right = pygame.K_RIGHT
keybind_up = pygame.K_UP
keybind_down = pygame.K_DOWN

async def main():
    # Initalizes the pygame 
    pygame.init()
    # makes the screen with out hardcoded values
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

    running = True

    while running:
        # Checks that pygame is still running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(BACKGROUND_COLOR)   # makes the window have a black background
        pygame.draw.circle(screen, (255, 0, 0), (400, 300), 50)

        pygame.display.flip() # displays the drawing
        await asyncio.sleep(0)

        

    pygame.quit()



if __name__ == "__main__":
    asyncio.run(main())



# Game classes and logic will be added below
