import pygame

from asciisim.res import IMG_DIR
from .sprite import AbstractSprite
from .sprite_position import SpritePosition
from pygame import Surface


class SpeechBubble(object):
    def __init__(self, sprite: AbstractSprite):
        self.sprite = sprite
        self.image_up = pygame.image.load(IMG_DIR + "speech_bubbles/up.png")
        self.image_down = pygame.image.load(IMG_DIR + "speech_bubbles/down.png")

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
        if self.sprite.position.y == 0:
            return self.image_down

        return self.image_up
