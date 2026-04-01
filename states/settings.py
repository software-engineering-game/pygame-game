import pygame

WIDTH, HEIGHT = 720, 720
TITLE = "Space Dodgers"
FPS = 60

# Keybinds
keybind_player_up = pygame.K_UP
keybind_player_down = pygame.K_DOWN
keybind_player_left = pygame.K_LEFT
keybind_player_right = pygame.K_RIGHT
keybind_player_shoot = pygame.K_SPACE

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
BULLET_SPEED = 8
BULLET_COOLDOWN = 0.2  # seconds between shots
