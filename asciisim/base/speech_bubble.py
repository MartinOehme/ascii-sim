import pygame
from pygame import Rect
from pygame import Surface

from ..res import IMG_DIR
from .game_object import GameObject
from .sprite import AbstractSprite


class SpeechBubble(GameObject):
    def __init__(self, sprite: AbstractSprite):
        super().__init__()
        self.content = None
        self.sprite = sprite
        self.register_surface(
            "up",
            lambda: pygame.image.load(IMG_DIR + "speech_bubbles/up.png")
        )
        self.register_surface(
            "down",
            lambda: pygame.image.load(IMG_DIR + "speech_bubbles/down.png")
        )

    @property
    def tile_rect(self) -> Rect:
        if self.sprite.tile_rect.top == 0:
            return Rect(
                self.sprite.tile_rect.left,
                self.sprite.tile_rect.top + 1,
                1, 1
            )

        return Rect(
            self.sprite.tile_rect.left,
            self.sprite.tile_rect.top - 1,
            1, 1
        )

    @tile_rect.setter
    def tile_rect(self, value):
        pass

    @property
    def image(self) -> Surface:
        surface = self.get_surface("up")
        if self.sprite.tile_rect.top == 0:
            surface = self.get_surface("down")

        if self.content:
            surface = surface.copy()
            surface.blit(
                self.content.image,
                (
                    17.5 * self.SCALING,
                    17.5 * self.SCALING
                )
            )

        return surface
