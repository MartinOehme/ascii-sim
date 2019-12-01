import pygame
from pygame import Rect

from ..base.context import Context
from ..sprites.static_sprite import AbstractSprite
from ..sprites.sprite_enums import MusicTracks


class Radiator(AbstractSprite):
    def __init__(self, temperature=22):
        super().__init__()
        self.tile_rect = Rect(3, 6, 2, 1)
        self.renderable = False

        self.temperature = temperature

    def update(self, context: Context):
        context.rooms["bar"].temperature = self.temperature

    def change_temperature(self, value):
        self.temperature += value


class MusicBox(AbstractSprite):
    def __init__(self, rect: Rect, track: MusicTracks = MusicTracks.MUSIC_OFF, volume=50):
        super().__init__()
        self.tile_rect = Rect(8, 1, 1, 1)
        self.renderable = False
        self.obstacle = True

        self.track: MusicTracks = track
        self.volume = volume

        if self.track is not MusicTracks.MUSIC_OFF:
            pygame.mixer_music.load(self.track.value)
            pygame.mixer_music.play(loops=-1)

    def update(self, context: Context):
        context.rooms["bar"].track = self.track
        context.rooms["bar"].volume = self.volume

        pygame.mixer_music.set_volume(self.volume/100)

    def change_volume(self, value):
        if 0 < self.volume < 100:
            self.volume += value
        elif (value > 0 and self.volume == 0) or (value < 0 and self.volume == 100):
            self.volume += value

    def change_music(self, track: MusicTracks):
        pygame.mixer_music.fadeout(2000)
        if track is MusicTracks.MUSIC_OFF:
            pygame.mixer_music.stop()
        else:
            pygame.mixer_music.load(track.value)
            pygame.mixer_music.play(loops=-1)

        self.track = track
