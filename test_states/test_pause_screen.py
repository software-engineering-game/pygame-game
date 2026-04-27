import os
import sys
# this replaces mocks with the real confirm quit state,
# which is needed to test the transition to it from the pause screen
from unittest.mock import patch
from states.game_state import GameState

import pygame


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# Ensure relative asset paths (e.g. fonts) resolve during tests.
os.chdir(PROJECT_ROOT)

pygame.init()
pygame.display.set_mode((1, 1))  # PauseScreen loads fonts; needs a display

from states.pause_state import PauseScreen


class FakeApp:
    def __init__(self):
        self.width = 800
        self.height = 600
        # Minimal stand-in for the real App object.
        # PauseScreen expects an `app.screen` surface to exist (for rendering).
        self.screen = pygame.display.get_surface()
        # Tests assign/inspect `app.state` to verify resume behavior.
        self.state = None
        # Tests inspect `changed_to` to verify state-transition requests.
        self.changed_to = None
        self.testing = True

    def change_state(self, new_state):
        # Mirror the real app API used by PauseScreen; record the requested state.
        self.changed_to = new_state


class DummyPreviousState:
    pass


def _make_pause_screen():
    # Factory helper to create a PauseScreen with a dummy previous state.
    # Keeps tests focused on behavior (events -> state changes) rather than setup.
    app = FakeApp()
    previous_state = DummyPreviousState()
    pause_screen = PauseScreen(app, previous_state)
    return app, pause_screen, previous_state


def test_escape_resumes_previous_state():
    # Pressing ESC should resume the game by restoring the previous state.
    app, pause_screen, previous_state = _make_pause_screen()
    app.state = pause_screen

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
    pause_screen.handle_event(app, event)

    assert app.state is previous_state


def test_click_resume_resumes_previous_state():
    # Clicking the Resume button should restore the previous state.
    app, pause_screen, previous_state = _make_pause_screen()
    app.state = pause_screen

    pause_screen.selected_index = 0

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    pause_screen.handle_event(app, event)

    assert app.state is previous_state


def test_click_quit_changes_to_confirm_quit_state():
    # Clicking Quit should request a transition to ConfirmQuitState.
    # Patch the real ConfirmQuitState to avoid importing/initializing extra UI.
    app, pause_screen, _previous_state = _make_pause_screen()

    class DummyConfirmQuitState:
        def __init__(self, previous_state):
            self.previous_state = previous_state

    pause_screen.selected_index = 2

    with patch("states.confirm_quit_state.ConfirmQuitState", DummyConfirmQuitState):
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
        pause_screen.handle_event(app, event)

    assert isinstance(app.changed_to, DummyConfirmQuitState)
    assert app.changed_to.previous_state is pause_screen


def test_click_main_menu_changes_to_main_menu_state():
    # Clicking Main Menu should request a transition to MainMenuState.
    app, pause_screen, _previous_state = _make_pause_screen()

    class DummyMainMenuState:
        pass

    pause_screen.selected_index = 1

    with patch("states.pause_state.MainMenuState", DummyMainMenuState):
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
        pause_screen.handle_event(app, event)

    assert isinstance(app.changed_to, DummyMainMenuState)


def test_game_state_transitions_to_pause_on_escape():
    # Clicking ESC from GaneState shopud make pause menu pop up
    app = FakeApp()

    game_state = GameState()
    game_state.on_enter(app)

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)

    game_state.handle_event(app, event)

    from states.pause_state import PauseScreen
    assert isinstance(app.changed_to, PauseScreen)