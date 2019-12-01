import pygame

from pygame.rect import Rect

from asciisim.sprites.sprite_enums import MachineStates
from ..base.context import Context
from ..base.sprite import AbstractSprite
from ..sprites.bar_keeper import BarKeeper


class CoffeeStorage(AbstractSprite):
    def __init__(self):
        super().__init__()
        self.tile_rect = Rect(0, 3, 2, 1)
        self.obstacle = True
        self.renderable = False
        self.state = None

    def update(self, context: Context):
        for event in context.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                for sprite in context.current_room.sprites:
                    if type(sprite) == BarKeeper:
                        if sprite.is_near(self):
<<<<<<< HEAD
                            sprite.item = self.state
                            context.closeup = self.closeup
=======
                            sprite.item = MachineStates.REFILL_COFFEE
>>>>>>> aea52c122baabedb10093b8e53c867c12126cfc8
