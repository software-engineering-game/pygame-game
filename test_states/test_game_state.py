import sys
import os
import pygame
from states.game_state import Bullet

# Add project root to Python path so tests can import from 'states'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


pygame.init()
pygame.display.set_mode((1, 1))  # tiny window to test the asset since it needs a display

#----------Bullet Tests----------
def test_bullet_despawn():
    bullet = Bullet("assets", "basic_bullet.png", 5, (100,100), (0,-1))

    bullet.rect.y = -100
    bullet.update()
    assert not bullet.alive()

def bullet_moves_up():
    bullet = Bullet("assets", "basic_bullet.png", 5, (100,100), (0,-1))

    start_y = bullet.rect.y
    bullet.update()
    assert bullet.rect.y > start_y

def bullets_alive_onscreen():
    bullet = Bullet("assets", "basic_bullet.png", 5, (100,100), (0,-1))

    bullet.update()
    assert bullet.alive()
