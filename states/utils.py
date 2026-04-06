import pygame
import os
import json
from typing import Type
from states import settings

# This exists to key out spritesheet backgrounds
SHEET_BG = (160, 200, 152)
FRAME_SIZE = 64

repo_root = os.path.dirname(os.path.dirname(__file__))
asset_folder = os.path.join(repo_root, "assets")

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
def load_spritesheet(sheet_name, frame_width, frame_height):
    sprite_sheet = pygame.image.load(os.path.join(asset_folder, sheet_name)).convert()
    sprite_sheet.set_colorkey(SHEET_BG)
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

def load_all_levels():
    try:
        with open(LEVEL_DATA, "r") as file:
            data = json.load(file)
            return data if isinstance(data, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def get_level_sequence():
    levels = load_all_levels()
    # Skip test/debug levels from normal progression flow.
    playable_levels = {
        level_name: level_data
        for level_name, level_data in levels.items()
        if "test" not in level_name.lower()
    }
    sorted_levels = sorted(
        playable_levels.items(),
        key=lambda item: item[1].get("level_num", 999999)
    )
    return [level_name for level_name, _ in sorted_levels]

def spawn_enemy_wave(enemy_type, enemy_group, frames, corner_pos, size, spacing):
    for j in range(size[1]):     # Rows
            for i in range(size[0]): # Columns
                (x, y) = (
                    corner_pos[0] + i * spacing[0],
                    corner_pos[1] + j * spacing[1]
                )
                enemy = enemy_type(frames=frames, start_pos=(x, y))
                enemy.rect.clamp_ip(pygame.Rect(0, 0, settings.WIDTH, settings.HEIGHT))
                enemy_group.add(enemy)

def build_level(level_name, enemy_ships, wave_index=None):
    # Loads the data for one level as a python dictionary
    level = load_level(level_name=level_name)
    if not level:
        raise ValueError(f"Unknown level: {level_name}")

    # Loads the background image named in level_data into a pygame image
    bg_image = pygame.image.load(os.path.join(asset_folder, level["bg_img"]))

    # Import locally to avoid circular imports (entities -> utils for spritesheets)
    from states import entities

    enemy_type_map: dict[str, Type[pygame.sprite.Sprite]] = {
        "Basic_Enemy": entities.Basic_Enemy,
        "Swarm_Enemy": entities.Swarm_Enemy,
        "Bomber_Enemy": entities.Bomber_Enemy,
    }

    # Spawns enemy waves (or one specific wave when wave_index is set)
    if wave_index is None:
        waves_to_spawn = level["waves"]
    else:
        waves = level["waves"]
        if wave_index < 0 or wave_index >= len(waves):
            raise ValueError(f"Wave index {wave_index} out of range for level '{level_name}'")
        waves_to_spawn = [waves[wave_index]]

    for wave in waves_to_spawn:
        enemy_type_name = wave.get("enemy_type")
        enemy_type = enemy_type_map.get(enemy_type_name)
        if enemy_type is None:
            raise ValueError(f"Unknown enemy_type '{enemy_type_name}' in level '{level_name}'")

        spawn_enemy_wave(
            enemy_type=enemy_type,
            enemy_group=enemy_ships,
            frames=load_spritesheet(
                sheet_name=wave["sprite_sheet"],
                frame_width=66,
                frame_height=FRAME_SIZE
            ),
            corner_pos=wave["wave_position"],
            size=wave["wave_size"],
            spacing=wave["wave_spacing"]
        )
    
    # Returns the background image name to tie it into level data
    return bg_image
