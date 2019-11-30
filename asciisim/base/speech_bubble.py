import pygame
from pygame import Surface

from ..res import IMG_DIR
from .game_object import GameObject
from .sprite import AbstractSprite
from .sprite_position import SpritePosition


class SpeechBubble(GameObject):
    def __init__(self, sprite: AbstractSprite):
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
    def position(self) -> SpritePosition:
        if self.sprite.position.y == 0:
            return SpritePosition(
                self.sprite.position.x,
                self.sprite.position.y + 1
            )

        return SpritePosition(
            self.sprite.position.x,
            self.sprite.position.y - 1
        )

    @property
    def image(self) -> Surface:
        surface = self.get_surface("up")
        if self.sprite.position.y == 0:
            surface = self.get_surface("down")

        if self.content:
            surface = surface.copy()
            surface.blit(
                self.content.image,
                (10, 10)
            )

        return surface
