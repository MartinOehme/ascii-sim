import pygame
from pygame.rect import Rect

from ..base.context import Context
from ..base.sprite import AbstractSprite
from ..sprites.bar_keeper import BarKeeper


class Item(AbstractSprite):
    def __init__(self, x: int, y: int, w: int, h: int, state):
        super().__init__()
        self.tile_rect = Rect(x, y, w, h)
        self.state = state
        self.obstacle = True
        self.renderable = False

    def update(self, context: Context):
        for event in context.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                for sprite in context.current_room.sprites:
                    if type(sprite) == BarKeeper:
                        if sprite.looks_at(self):
                            sprite.item = self.state
