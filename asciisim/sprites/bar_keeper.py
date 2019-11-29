import pygame
from pygame import Surface

from ..base.sprite import AbstractSprite
from ..base.context import Context
from ..base.sprite_position import SpritePosition
from ..res import IMG_DIR

class BarKeeper(AbstractSprite):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__()
        self.position = SpritePosition(x, y)
        self.image = pygame.image.load(IMG_DIR + "bar_keeper.png")

    def update(self, context: Context):
        for event in context.events:
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_UP and self.position.y > 0:
                self.position.y -= 1
            elif event.key == pygame.K_DOWN and self.position.y < 6:
                self.position.y += 1
            elif event.key == pygame.K_LEFT:
                if (self.position.x == 0
                      and self.position.y == 6
                      and context.room_key == Context.STORE_ROOM):
                    context.set_room(Context.BAR_ROOM)
                elif self.position.x > 0:
                    self.position.x -= 1
            elif event.key == pygame.K_RIGHT:
                if (self.position.x == 9
                    and self.position.y == 6
                    and context.room_key == Context.BAR_ROOM):
                    context.set_room(Context.STORE_ROOM)
                elif self.position.x < 9:
                    self.position.x += 1
