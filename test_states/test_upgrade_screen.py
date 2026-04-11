import os
import sys
from unittest.mock import patch

import pygame


# allows us to run pytest in different directories
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
	sys.path.append(PROJECT_ROOT)

# Ensure relative asset paths resolve during tests.
os.chdir(PROJECT_ROOT)


pygame.init()
pygame.display.set_mode((1, 1))  # UpgradeState can render text; needs a display


from states import settings
from states.upgrade_state import UpgradeState


class FakeApp:
	def __init__(self):
		self.changed_to = None

	def change_state(self, state):
		self.changed_to = state


class FakePreviousState:
	def __init__(self):
		self.draw_calls = 0

	def draw(self, app, screen):
		self.draw_calls += 1


class _DummyFont:
	def __init__(self, size):
		self.size = size

	def render(self, text, antialias, color):
		# Return a surface large enough that get_rect/center work.
		surface = pygame.Surface((max(10, len(text) * 5), 20))
		surface.fill((0, 0, 0))
		return surface


def _make_state():
	app = FakeApp()
	previous = FakePreviousState()
	state = UpgradeState(app, previous)

	# Patch font loading so tests don't depend on local font availability.
	with patch("pygame.font.Font", side_effect=lambda _path, size: _DummyFont(size)):
		state.on_enter(app)

	return app, previous, state


def test_on_enter_initializes_selection_and_options():
	_app, _previous, state = _make_state()

	assert state.selected == 0
	assert state.options == ["Bullet Speed +2", "Fire Rate +10%"]
	assert state.font is not None
	assert state.small_font is not None


def test_up_or_down_toggles_selected_option():
	app, _previous, state = _make_state()

	assert state.selected == 0

	event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
	state.handle_event(app, event)
	assert state.selected == 1

	event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
	state.handle_event(app, event)
	assert state.selected == 0


def test_enter_applies_bullet_speed_upgrade_and_returns_to_previous():
	app, previous, state = _make_state()

	original_speed = settings.BULLET_SPEED
	try:
		state.selected = 0
		event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
		state.handle_event(app, event)

		assert settings.BULLET_SPEED == 15
		assert app.changed_to is previous
	finally:
		settings.BULLET_SPEED = original_speed


def test_space_applies_cooldown_upgrade_and_returns_to_previous():
	app, previous, state = _make_state()

	original_cooldown = settings.BULLET_COOLDOWN
	try:
		state.selected = 1
		event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
		state.handle_event(app, event)

		assert settings.BULLET_COOLDOWN == 0.3
		assert app.changed_to is previous
	finally:
		settings.BULLET_COOLDOWN = original_cooldown


def test_escape_returns_to_previous_without_applying_upgrades():
	app, previous, state = _make_state()

	original_speed = settings.BULLET_SPEED
	original_cooldown = settings.BULLET_COOLDOWN

	event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
	state.handle_event(app, event)

	assert app.changed_to is previous
	assert settings.BULLET_SPEED == original_speed
	assert settings.BULLET_COOLDOWN == original_cooldown


def test_non_keydown_events_do_nothing():
	app, _previous, state = _make_state()

	event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(0, 0))
	state.handle_event(app, event)

	assert app.changed_to is None


def test_draw_calls_previous_state_draw_and_renders_overlay():
	app, previous, state = _make_state()

	# Provide a surface to draw onto.
	screen = pygame.Surface((settings.WIDTH, settings.HEIGHT))

	# Re-patch font in case any test runner reorders execution.
	with patch("pygame.font.Font", side_effect=lambda _path, size: _DummyFont(size)):
		state.draw(app, screen)

	assert previous.draw_calls == 1
