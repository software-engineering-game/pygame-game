import pygame
import os
import json

#
# High Score
#

SCORE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "highscore.json")

def load_high_score():
    try:
        with open(SCORE_FILE, "r") as f:
            data = json.load(f)
            return data.get("high_score", 0)
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return 0

def save_high_score(score):
    current_best = load_high_score()
    if score > current_best:
        with open(SCORE_FILE, "w") as f:
            json.dump({"high_score": score}, f)
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

def build_level(level_data):
    pass
