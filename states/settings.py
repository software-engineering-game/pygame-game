import pygame

WIDTH, HEIGHT = 720, 720
TITLE = "Space Dodgers"
FPS = 60

# Options page settings
CONTROL_SCHEME = "WASD" # or ARROWS
SFX_ON = True
MUSIC_ON = True

# Keybinds
keybind_player_up = pygame.K_UP
keybind_player_down = pygame.K_DOWN
keybind_player_left = pygame.K_LEFT
keybind_player_right = pygame.K_RIGHT
keybind_player_shoot = pygame.K_SPACE
keybind_menu_confirm = pygame.K_RETURN # The enter key
keybind_menu_exit = pygame.K_ESCAPE    # The escape key
keybind_debug_shop = pygame.K_t
keybind_upgrade_1 = pygame.K_1
keybind_upgrade_2 = pygame.K_2

def set_controls_arrows():
    global CONTROL_SCHEME
    global keybind_player_up, keybind_player_down, keybind_player_left, keybind_player_right

    CONTROL_SCHEME = "ARROWS"
    keybind_player_up = pygame.K_UP
    keybind_player_down = pygame.K_DOWN
    keybind_player_left = pygame.K_LEFT
    keybind_player_right = pygame.K_RIGHT

def set_controls_wasd():
    global CONTROL_SCHEME
    global keybind_player_up, keybind_player_down, keybind_player_left, keybind_player_right

    CONTROL_SCHEME = "WASD"
    keybind_player_up = pygame.K_w
    keybind_player_down = pygame.K_s
    keybind_player_left = pygame.K_a
    keybind_player_right = pygame.K_d

def toggle_controls():
    if CONTROL_SCHEME == "WASD":
        set_controls_wasd()
    else:
        set_controls_arrows()


def toggle_sfx():
    global SFX_ON
    SFX_ON = not SFX_ON


def toggle_music():
    global MUSIC_ON
    MUSIC_ON = not MUSIC_ON

# Enemy Variables
basic_enemy_spd = 2
swarm_enemy_spd = 3
bomber_enemy_spd = 1

# optional wave defaults
WAVE_COLUMNS = 5
WAVE_ROWS = 2
WAVE_X_SPACING = 80
WAVE_Y_SPACING = 80
WAVE_CORNER_X = 120
WAVE_CORNER_Y = 120

# Bullet settings
DEFAULT_BULLET_SPEED = 13
DEFAULT_BULLET_COOLDOWN = 0.3  # seconds between shots

# runtime-tuned by upgrades
bullet_spd = DEFAULT_BULLET_SPEED
bullet_cooldown = DEFAULT_BULLET_COOLDOWN
