import pygame
from pygame import Rect

from asciisim.sprites.bar_keeper import BarKeeper
from ..base.context import Context
from ..base.closeup import Closeup
from ..base.sprite import AbstractSprite
from ..sprites.sprite_enums import MusicTracks, OrderSitters

from ..res import IMG_DIR
from ..menu.menu import Menu
from ..menu.control import Control


class RadiatorCloseup(Closeup):
    def __init__(self, radiator: 'Radiator'):
        super().__init__(IMG_DIR + "radiator/radiator_closeup.png")
        self.radiator = radiator
        self.menu = Menu()
        self.menu.add_control(Control(710, 350, 140, 140))  # 0 -> temperature up
        self.menu.add_control(Control(710, 490, 140, 130))  # 1 -> temperature down

        self.sprites += self.menu.control_sprites

    def update(self, context: Context) -> None:
        self.menu.update(context)
        for event in context.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.radiator.change_temperature(self.menu.control_index)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                context.closeup = None


class MusicBoxCloseup(Closeup):
    def __init__(self, music_box: 'MusicBox'):
        super().__init__(IMG_DIR + "music_box/music_box_closeup.png")
        self.music_box = music_box
        self.menu = Menu()
        self.menu.add_control(Control(778, 435, 337, 337))  # 0 -> music off
        self.menu.add_control(Control(1390, 530, 150, 150))  # 1 -> previous track
        self.menu.add_control(Control(1583, 530, 150, 150))  # 2 -> next track
        self.menu.add_control(Control(626, 530, 150, 150))  # 3 -> volume down
        self.menu.add_control(Control(1115, 530, 150, 150))  # 4 -> volume up

        self.sprites += self.menu.control_sprites

    def update(self, context: Context) -> None:
        self.menu.update(context)
        for event in context.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.menu.control_index == 0:
                    self.music_box.change_music(MusicTracks.MUSIC_OFF)
                elif self.menu.control_index == 1:
                    self.music_box.change_music(MusicTracks.TRACK1)
                elif self.menu.control_index == 2:
                    self.music_box.change_music(MusicTracks.TRACK2)
                elif self.menu.control_index == 3:
                    self.music_box.change_volume(-2)
                elif self.menu.control_index == 4:
                    self.music_box.change_volume(2)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                context.closeup = None


class Radiator(AbstractSprite):
    def __init__(self, rect: Rect = Rect(3, 6, 2, 1), temperature: int = 22):
        super().__init__()
        self.tile_rect = rect
        self.renderable = False
        self.obstacle = True
        self.closeup = RadiatorCloseup(self)

        self.temperature: int = temperature

    def update(self, context: Context):
        context.rooms["bar"].temperature = self.temperature

        for event in context.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                for sprite in context.current_room.sprites:
                    if type(sprite) == BarKeeper:
                        if sprite.looks_at(self):
                            context.closeup = self.closeup

    def change_temperature(self, value):
        self.temperature += (1 - 2 * value)


class MusicBox(AbstractSprite):
    def __init__(self, rect: Rect = Rect(8, 1, 2, 1), track: MusicTracks = MusicTracks.MUSIC_OFF, volume=50):
        super().__init__()
        self.tile_rect = rect
        self.renderable = False
        self.obstacle = True
        self.closeup = MusicBoxCloseup(self)

        self.track: MusicTracks = track
        self.volume = volume

        if self.track is not MusicTracks.MUSIC_OFF:
            pygame.mixer_music.load(self.track.value)
            pygame.mixer_music.play(loops=-1)

    def update(self, context: Context):
        context.rooms["bar"].track = self.track
        context.rooms["bar"].volume = self.volume
        pygame.mixer_music.set_volume(self.volume / 100)

        for event in context.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                for sprite in context.current_room.sprites:
                    if type(sprite) == BarKeeper:
                        if sprite.looks_at(self):
                            context.closeup = self.closeup

    def change_volume(self, value):
        if 0 < self.volume < 100:
            self.volume += value
        elif (value > 0 and self.volume == 0) or (value < 0 and self.volume == 100):
            self.volume += value
        pygame.mixer_music.set_volume(self.volume / 100)

    def change_music(self, track: MusicTracks):
        pygame.mixer_music.fadeout(500)
        if track is MusicTracks.MUSIC_OFF:
            pygame.mixer_music.stop()
        else:
            pygame.mixer_music.load(track.value)
            pygame.mixer_music.play(loops=-1)

        self.track = track
