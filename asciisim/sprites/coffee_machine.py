import pygame

from .sprite_enums import States

from .static_sprite import StaticSprite
from ..base.sprite_position import SpritePosition
from ..base.context import Context
from ..res import IMG_DIR


class CoffeeMachine(StaticSprite):
    def __init__(self):
        super().__init__(
            SpritePosition(0, 0),
            pygame.image.load(IMG_DIR + "coffee_machine.png")
        )

    def useSprite(self, state: States):
        if state
