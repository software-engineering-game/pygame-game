import pygame
import os
from states import settings

repo_root = os.path.dirname(os.path.dirname(__file__))

# global volume variable
VOLUME = 0.25


class music_manager:
    TRACKS = {
        "game": os.path.join(repo_root, "assets", "song_ogg", "gamedemo.ogg"),
        "menu": os.path.join(repo_root, "assets", "song_ogg", "hometheme.ogg"),
        "gameover": os.path.join(repo_root, "assets", "song_ogg", "gameover.ogg")
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

        pygame.mixer.music.set_volume(VOLUME)

        pygame.mixer.music.play(loops)
        self.current_track = path

    def stop(self):
        pygame.mixer.music.stop()
        self.current_track = None