import pygame
import os
import json

# This exists to key out spritesheet backgrounds
SHEET_BG = (160, 200, 152)
FRAME_SIZE = 64

#
# High Score
#

SCORE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "highscore.json")

def load_high_score():
    try:
        with open(SCORE_FILE, "r") as file:
            data = json.load(file)
            return data.get("high_score", 0)
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return 0

def save_high_score(score):
    current_best = load_high_score()
    if score > current_best:
        with open(SCORE_FILE, "w") as file:
            json.dump({"high_score": score}, file)
        return True
    return False

#
# General Utility
#

# Takes a spritesheet and splits it into a list of frames
# Returns the frames as a list of pygame images
def load_spritesheet(asset_folder, sheet_name, key_color, frame_width, frame_height):
    sprite_sheet = pygame.image.load(os.path.join(asset_folder, sheet_name)).convert()
    sprite_sheet.set_colorkey(key_color)
    frames = []
    for j in range(0, sprite_sheet.get_height(), frame_height):
        for i in range(0, sprite_sheet.get_width(), frame_width):
            rect = pygame.Rect(i, j, frame_width, frame_height)
            image = pygame.Surface(rect.size, pygame.SRCALPHA)
            image.blit(sprite_sheet, (0, 0), rect)
            frames.append(image)
    return frames

#
# Loading Level Data
#

LEVEL_DATA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "level_data.json")

def load_level(level_name):
    try:
        with open(LEVEL_DATA, "r") as file:
            data = json.load(file)
            return data.get(level_name)
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return 0



def spawn_enemy_wave(enemy_type, enemy_group, frames, corner_pos, size, spacing):
    for j in range(size[1]):     # Rows
            for i in range(size[0]): # Columns
                (x, y) = (
                    corner_pos[0] + i * spacing[0],
                    corner_pos[1] + j * spacing[1]
                )
                enemy = enemy_type(frames=frames, start_pos=(x, y))
                enemy_group.add(enemy)

def build_level(asset_folder, level_name, enemy_ships, temp_type):
    # Loads the data for one level as a python dictionary
    level = load_level(level_name=level_name)

    # Loads the background image named in level_data into a pygame image
    bg_image = pygame.image.load(os.path.join(asset_folder, level["bg_img"]))
    
    #needs to parse enemy types from level_data somehow

    # Spawns enemy waves
    # Loops for however many waves there are
    for wav_index in range(len(level["waves"])):
        
        
        spawn_enemy_wave(
            enemy_type=temp_type,
            enemy_group=enemy_ships,
            frames=load_spritesheet(
                asset_folder=asset_folder,
                sheet_name=level["waves"][wav_index]["sprite_sheet"],
                key_color=SHEET_BG,
                frame_width=66,
                frame_height=FRAME_SIZE
            ),
            corner_pos=level["waves"][wav_index]["wave_position"],
            size=level["waves"][wav_index]["wave_size"],
            spacing=level["waves"][wav_index]["wave_spacing"]
        )
    
    # Returns the background image name to tie it into level data
    return bg_image
