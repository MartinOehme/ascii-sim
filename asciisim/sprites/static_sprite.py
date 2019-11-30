from pygame import Surface

from ..base.sprite import AbstractSprite
from ..base.context import Context
from ..base.sprite_position import SpritePosition


class StaticSprite(AbstractSprite):
    def __init__(self, position: SpritePosition, image: Surface):
        super().__init__()
        self.position = position
        self.image = image

    def update(self, context: Context):
        pass

    def use_sprite(self):
        pass