import os
import sys
import pygame


# Add project root to Python path so tests can import from 'states'
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# allows us to run pytest in different directories
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT) 
# Myah added this 

# Ensure relative asset paths resolve during tests.
os.chdir(PROJECT_ROOT)

from states.death_state import DeathState
from states.entities import Bullet
from states.game_state import GameState

pygame.init()
pygame.display.set_mode((1, 1))  # tiny window to test the asset since it needs a display

# Fake app for testing
class FakeApp:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.changed_to = None
        self.testing = True

    def change_state(self, state):
        self.changed_to = state

#----------Bullet Tests----------

def test_bullet_despawn():
    bullet = Bullet("assets", "basic_bullet.png", 5, (100,100), (0,-1))

    bullet.rect.y = -100
    bullet.update()
    assert not bullet.alive()

def test_bullet_moves_up():
    bullet = Bullet("assets", "basic_bullet.png", 5, (100,100), (0,-1))

    start_y = bullet.rect.y
    bullet.update()
    assert bullet.rect.y < start_y

def test_bullets_alive_onscreen():
    bullet = Bullet("assets", "basic_bullet.png", 5, (100,100), (0,-1))

    group = pygame.sprite.Group()
    group.add(bullet)
    
    bullet.update()
    assert bullet.alive()

#----------Player Death Test----------

def test_player_dies_on_collision():  
    app = FakeApp()

    game_state = GameState()
    game_state.on_enter(app)

    # moves the enemy into the player
    enemy = next(iter(game_state.enemy_ships))
    enemy.rect.center = game_state.player.rect.center

    game_state.update(app, dt=0.016)

    assert isinstance(app.changed_to, DeathState)

#----------Game State Initialization Test----------

def test_game_state_init():
    game_state = GameState()
    game_state.on_enter(FakeApp())

    assert game_state.player is not None
    assert len(game_state.enemy_ships) > 0

#----------Player Stays In Bounds Test----------

def player_stays_in_bounds():
    game_state = GameState()
    game_state.on_enter(FakeApp())

    # forces the player out of bounds
    game_state.player.x = -100
    game_state.player.y = -100

    assert game_state.player.rect.left >= 0
    assert game_state.player.rect.right >= 0

#----------Enemy hit counter increase Test----------

def test_enemy_hit_counter_increments():
    app = FakeApp()

    game_state = GameState()
    game_state.on_enter(app)

    enemy = next(iter(game_state.enemy_ships))

    bullet = pygame.sprite.Sprite()
    bullet.rect = enemy.rect.copy()

    game_state.ally_bullets.add(bullet)

    assert game_state.enemy_hit_count == 0

    game_state.update(app, dt=0.016)

    assert game_state.enemy_hit_count == 1


