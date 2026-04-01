import os
import sys
import pygame

from states.confirm_quit_state import ConfirmQuitState

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

class DummyPreviousState():
    def __init__(self):
        self.width = 800
        self.height = 600
        self.changed_to = None

    def change_state(self, state):
        self.changed_to = state


def test_confirm_quit_sets_running_false():
    app = FakeApp()
    app.running = True  # simulate app running

    previous_state = DummyPreviousState()
    state = ConfirmQuitState(previous_state)
    state.on_enter(app)

    # Ensure "Yes" is selected (index 0)
    state.selected = 0

    # Simulate pressing ENTER
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    state.handle_event(app, event)

    assert app.running is False