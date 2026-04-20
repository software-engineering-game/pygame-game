import pygame
import os
from states import settings

repo_root = os.path.dirname(os.path.dirname(__file__))

class music_manager:
    TRACKS = {
        "game": os.path.join(repo_root, "assets", "song_ogg", "gamedemo.ogg"),
    }

    def __init__(self):
        self.current_track = None

    def play_track(self, name, loops=-1):
        if not settings.MUSIC_ON:
            return
        path = self.TRACKS.get(name)
        if not path:
            return

        if self.current_track == path and pygame.mixer.music.get_busy():
            return

        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(loops)
        self.current_track = path

    def stop(self):
        pygame.mixer.music.stop()
        self.current_track = None