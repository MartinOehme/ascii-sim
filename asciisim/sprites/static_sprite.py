from pygame import Surface

from .sprite_enums import States

from ..base.sprite import AbstractSprite
from ..base.context import Context
from ..base.sprite_position import SpritePosition


class StaticSprite(AbstractSprite):
    def __init__(self, position: SpritePosition, image: Surface):
        super().__init__()
        self.position = position
        self.image = image
        self.state: States = States.NOT_USED

    def update(self, context: Context):
        if self.state is not States.NOT_USED:
            self.use_sprite(self.state)

    def use_sprite(self, state: States):
        pass
