import pygame
from pygame import Rect

from asciisim.sprites.bar_keeper import BarKeeper
from ..base.context import Context
from ..base.closeup import Closeup
from ..sprites.static_sprite import AbstractSprite
from ..sprites.sprite_enums import MusicTracks, OrderSitters

from ..res import IMG_DIR
from ..menu.menu import Menu
from ..menu.control import Control


class RadiatorCloseup(Closeup):
    def __init__(self, radiator: 'Radiator'):
        super().__init__(IMG_DIR + "radiator/radiator_closeup.png")
        self.radiator = radiator
        self.menu = Menu()
        self.menu.add_control(Control(900, 400, 400, 100))
        self.menu.add_control(Control(900, 600, 400, 100))

        self.sprites += self.menu.control_sprites

    def update(self, context: Context) -> None:
        self.menu.update(context)
        for event in context.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                for sprite in context.current_room.sprites:
                    if type(sprite) == BarKeeper:
                        if self.menu.control_index == 0:
                            sprite.item = OrderSitters.TEMPERATURE_UP
                        elif self.menu.control_index == 1:
                            sprite.item = OrderSitters.TEMPERATURE_UP

                    context.closeup = None

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                context.closeup = None

class MusicBoxCloseup(Closeup):
    pass


class Radiator(AbstractSprite):
    def __init__(self, temperature=22):
        super().__init__()
        self.tile_rect = Rect(3, 6, 2, 1)
        self.renderable = False
        self.obstacle = True
        self.closeup = RadiatorCloseup(self)

        self.temperature = temperature

    def update(self, context: Context):
        context.rooms["bar"].temperature = self.temperature
        for event in context.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                for sprite in context.current_room.sprites:
                    if type(sprite) == BarKeeper:
                        if sprite.looks_at(self):
                            context.closeup = self.closeup

    def change_temperature(self, value):
        self.temperature += value


class MusicBox(AbstractSprite):
    def __init__(self, rect: Rect, track: MusicTracks = MusicTracks.MUSIC_OFF, volume=50):
        super().__init__()
        self.tile_rect = Rect(8, 1, 1, 2)
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











class RefrigeratorCloseup(Closeup):
    def __init__(self, refrigeratore: 'Refrigerator'):
        super().__init__(IMG_DIR + "refrigeratore/refrigeratore_closeup.png")
        self.refrigeratore = refrigeratore
        self.menu = Menu()
        self.menu.add_control(Control(760, 200, 400, 100))
        self.menu.add_control(Control(760, 400, 400, 100))
        self.menu.add_control(Control(760, 600, 400, 100))

        self.sprites += self.menu.control_sprites

    def update(self, context: Context) -> None:
        self.menu.update(context)
        for event in context.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                for sprite in context.current_room.sprites:
                    if type(sprite) == BarKeeper:
                        if self.menu.control_index == 0:
                            sprite.item = OrderWalkers.KOLLE_MATE
                        elif self.menu.control_index == 1:
                            sprite.item = OrderWalkers.PREMIUM_COLA
                        elif self.menu.control_index == 2:
                            sprite.item = OrderWalkers.ZOTRINE

                    context.closeup = None

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                context.closeup = None


class Refrigerator(AbstractSprite):
    def __init__(self):
        super().__init__()
        self.closeup = RefrigeratorCloseup(self)
        self.tile_rect = Rect(0, 4, 2, 1)
        self.obstacle = True
        self.renderable = False
        self.state = None

    def update(self, context: Context):
        for event in context.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                for sprite in context.current_room.sprites:
                    if type(sprite) == BarKeeper:
                        if sprite.looks_at(self):
                            context.closeup = self.closeup