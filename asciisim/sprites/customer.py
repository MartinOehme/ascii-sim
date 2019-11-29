from pygame import Surface
from ..base.sprite import AbstractSprite
from ..base.context import Context
from ..base.sprite_position import SpritePosition


class CustomerSprite(AbstractSprite):
    def __init__(self, position: SpritePosition, image: Surface):
        super().__init__()
        self.position = position
        self.image = image

    def generate_wish(self, ):
        pass

    def spawn(self, context: Context):
        # TODO: Spawn in der Tür; Generation von Wünschen
        pass

    def update(self, context: Context):
        pass
