from pygame import Rect

from ..base.context import Context
from ..sprites.static_sprite import StaticSprite
from ..res import IMG_DIR
from ..sprites.sprite_enums import MusicTracks

class Radiator(StaticSprite):
    def __init__(self, rect: Rect, temperature=22):
        super().__init__(
            rect,
            IMG_DIR + "radiator.png"
        )

        self.temperature = temperature

    def update(self, context: Context):
        context.rooms["bar"].temperature = self.temperature

    def change_temperature(self, value):
        self.temperature += value


class MusicBox(StaticSprite):
    def __init__(self, rect: Rect, track: MusicTracks = MusicTracks.MUSIC_OFF, volume=50):
        super().__init__(
            rect,
            IMG_DIR + "music_box.png"
        )

        self.track: MusicTracks = track
        self.volume = volume

    def update(self, context: Context):
        context.rooms["bar"].track = self.track
        context.rooms["bar"].volume = self.volume

    def change_volume(self, value):
        self.volume += value

    def change_music(self):
        pass