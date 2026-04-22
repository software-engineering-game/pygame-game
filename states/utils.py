import pygame
import os
import json
import shutil
from typing import Type, Optional, Tuple, List, Dict, Any
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

# Returns a list of all the hitboxes from a sprite group
def extract_hitboxes(sprite_group):
    hitbox_list = []
    sprite_list = sprite_group.sprites()
    for i in range(len(sprite_list)):
        hitbox_list.append(sprite_list[i].hitbox)
    return hitbox_list

#
# Loading Level Data
#

LEVEL_DATA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "level_data.json")
CUSTOM_LEVEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "custom_level.json")
CUSTOM_LEVELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "custom_levels")

# Editor / play use fixed slots so filenames stay simple without a text field.
CUSTOM_LEVEL_SLOT_MIN = 1
CUSTOM_LEVEL_SLOT_MAX = 8

# Synthetic key for in-memory custom runs (not stored in level_data.json).
CUSTOM_LEVEL_KEY = "__custom__"

KNOWN_ENEMY_TYPES = frozenset({"Basic_Enemy", "Swarm_Enemy", "Bomber_Enemy"})

SPRITE_SHEET_BY_ENEMY_TYPE: Dict[str, str] = {
    "Basic_Enemy": "enemy_basic.png",
    "Swarm_Enemy": "enemy_swarm.png",
    "Bomber_Enemy": "enemy_bomber.png",
}

# Default positions/spacing per wave index for the simple level editor.
CUSTOM_WAVE_LAYOUT_PRESETS: List[Tuple[List[int], List[int]]] = [
    ([160, 100], [80, 80]),
    ([100, 140], [85, 80]),
    ([120, 220], [70, 80]),
    ([180, 300], [75, 75]),
]

CUSTOM_BACKGROUND_OPTIONS: Tuple[str, ...] = (
    "background_asteroids.png",
    "background_test.png",
)


def default_custom_level_dict():
    return {
        "level_num": 0,
        "bg_img": CUSTOM_BACKGROUND_OPTIONS[0],
        "waves": [
            {
                "enemy_type": "Basic_Enemy",
                "sprite_sheet": SPRITE_SHEET_BY_ENEMY_TYPE["Basic_Enemy"],
                "wave_position": list(CUSTOM_WAVE_LAYOUT_PRESETS[0][0]),
                "wave_size": [3, 2],
                "wave_spacing": list(CUSTOM_WAVE_LAYOUT_PRESETS[0][1]),
            }
        ],
    }


def editor_model_to_level_dict(editor_waves, bg_img: str) -> Dict[str, Any]:
    waves_out = []
    for i, wave in enumerate(editor_waves):
        pos, spacing = CUSTOM_WAVE_LAYOUT_PRESETS[i % len(CUSTOM_WAVE_LAYOUT_PRESETS)]
        enemy_type = wave["enemy_type"]
        waves_out.append(
            {
                "enemy_type": enemy_type,
                "sprite_sheet": SPRITE_SHEET_BY_ENEMY_TYPE[enemy_type],
                "wave_position": list(pos),
                "wave_size": [wave["cols"], wave["rows"]],
                "wave_spacing": list(spacing),
            }
        )
    return {"level_num": 0, "bg_img": bg_img, "waves": waves_out}


def editor_model_from_level_dict(level_dict: dict) -> Tuple[str, List[dict]]:
    bg = level_dict.get("bg_img", CUSTOM_BACKGROUND_OPTIONS[0])
    if bg not in CUSTOM_BACKGROUND_OPTIONS:
        bg = CUSTOM_BACKGROUND_OPTIONS[0]
    waves_in = level_dict.get("waves", [])
    editor_waves = []
    for w in waves_in:
        if not isinstance(w, dict):
            continue
        et = w.get("enemy_type", "Basic_Enemy")
        if et not in KNOWN_ENEMY_TYPES:
            et = "Basic_Enemy"
        size = w.get("wave_size", [3, 2])
        cols = int(size[0]) if len(size) > 0 else 3
        rows = int(size[1]) if len(size) > 1 else 2
        cols = max(1, min(8, cols))
        rows = max(1, min(4, rows))
        editor_waves.append({"enemy_type": et, "cols": cols, "rows": rows})
    if not editor_waves:
        editor_waves.append({"enemy_type": "Basic_Enemy", "cols": 3, "rows": 2})
    return bg, editor_waves


def ensure_custom_levels_dir():
    os.makedirs(CUSTOM_LEVELS_DIR, exist_ok=True)
    first_slot = path_for_custom_slot(1)
    if os.path.isfile(CUSTOM_LEVEL_PATH) and not os.path.isfile(first_slot):
        try:
            shutil.copy2(CUSTOM_LEVEL_PATH, first_slot)
        except OSError:
            pass


def path_for_custom_slot(slot: int) -> str:
    slot = max(CUSTOM_LEVEL_SLOT_MIN, min(CUSTOM_LEVEL_SLOT_MAX, int(slot)))
    return os.path.join(CUSTOM_LEVELS_DIR, "slot_{:02d}.json".format(slot))


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


def validate_level_dict(level_dict) -> Tuple[bool, Optional[str]]:
    if not isinstance(level_dict, dict):
        return False, "Level data must be an object"

    bg_img = level_dict.get("bg_img")
    if not isinstance(bg_img, str) or not bg_img.strip():
        return False, "Missing or invalid bg_img"

    waves = level_dict.get("waves")
    if not isinstance(waves, list) or len(waves) == 0:
        return False, "waves must be a non-empty list"

    for i, wave in enumerate(waves):
        if not isinstance(wave, dict):
            return False, f"Wave {i + 1} must be an object"

        enemy_type_name = wave.get("enemy_type")
        if enemy_type_name not in KNOWN_ENEMY_TYPES:
            return False, f"Unknown enemy_type in wave {i + 1}"

        for key in ("sprite_sheet", "wave_position", "wave_size", "wave_spacing"):
            if key not in wave:
                return False, f"Wave {i + 1} missing '{key}'"

        if not isinstance(wave["sprite_sheet"], str) or not wave["sprite_sheet"].strip():
            return False, f"Wave {i + 1} has invalid sprite_sheet"

        for key in ("wave_position", "wave_size", "wave_spacing"):
            val = wave[key]
            if (
                not isinstance(val, list)
                or len(val) != 2
                or not all(isinstance(n, (int, float)) for n in val)
            ):
                return False, f"Wave {i + 1} has invalid {key} (need [x, y])"

    return True, None


def load_custom_level_from_path(path: str) -> Tuple[Optional[dict], Optional[str]]:
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return None, "File not found"
    except json.JSONDecodeError:
        return None, "Not valid JSON"

    ok, err = validate_level_dict(data)
    if not ok:
        return None, err
    return data, None


def list_valid_custom_level_paths() -> List[str]:
    """Validated JSON level files in custom_levels/ (used by Play Custom)."""
    ensure_custom_levels_dir()
    paths: List[str] = []
    try:
        names = sorted(os.listdir(CUSTOM_LEVELS_DIR))
    except OSError:
        return paths
    for name in names:
        if not name.endswith(".json"):
            continue
        full = os.path.join(CUSTOM_LEVELS_DIR, name)
        if not os.path.isfile(full):
            continue
        data, _err = load_custom_level_from_path(full)
        if data is not None:
            paths.append(full)
    return paths


def friendly_name_for_custom_path(path: str) -> str:
    base = os.path.splitext(os.path.basename(path))[0]
    if base.startswith("slot_") and len(base) > 5:
        rest = base[5:]
        if rest.isdigit():
            return "Slot {}".format(int(rest))
    return base.replace("_", " ")


def load_custom_level() -> Tuple[Optional[dict], Optional[str]]:
    """Legacy path: repo root custom_level.json (tests and old flows)."""
    return load_custom_level_from_path(CUSTOM_LEVEL_PATH)


def save_custom_level_to_path(level_dict: dict, path: str) -> None:
    ok, err = validate_level_dict(level_dict)
    if not ok:
        raise ValueError(err or "Invalid level data")
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(level_dict, file, indent=3)


def save_custom_level(level_dict):
    """Legacy: write repo root custom_level.json."""
    save_custom_level_to_path(level_dict, CUSTOM_LEVEL_PATH)


def build_level_from_dict(level_dict, enemy_ships, level_label="custom"):
    ok, err = validate_level_dict(level_dict)
    if not ok:
        raise ValueError(err or "Invalid level data")

    bg_image = pygame.image.load(os.path.join(asset_folder, level_dict["bg_img"]))

    from states import entities

    enemy_type_map: Dict[str, Type[pygame.sprite.Sprite]] = {
        "Basic_Enemy": entities.Basic_Enemy,
        "Swarm_Enemy": entities.Swarm_Enemy,
        "Bomber_Enemy": entities.Bomber_Enemy,
    }

    for wave in level_dict["waves"]:
        enemy_type_name = wave.get("enemy_type")
        enemy_type = enemy_type_map.get(enemy_type_name)
        if enemy_type is None:
            raise ValueError(
                f"Unknown enemy_type '{enemy_type_name}' in level '{level_label}'"
            )

        spawn_enemy_wave(
            enemy_type=enemy_type,
            enemy_group=enemy_ships,
            frames=load_spritesheet(
                sheet_name=wave["sprite_sheet"],
                frame_width=66,
                frame_height=FRAME_SIZE,
            ),
            corner_pos=wave["wave_position"],
            size=wave["wave_size"],
            spacing=wave["wave_spacing"],
        )

    return bg_image


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

def build_level(level_name, enemy_ships):
    level = load_level(level_name=level_name)
    if not level:
        raise ValueError(f"Unknown level: {level_name}")
    return build_level_from_dict(level, enemy_ships, level_label=level_name)
