import pygame
from pygame import Surface

from ..base.sprite import AbstractSprite
from ..base.context import Context
from ..base.sprite_position import SpritePosition
from ..res import IMG_DIR

class BarKeeper(AbstractSprite):
    def __init__(self):
        super().__init__()
        self.position = SpritePosition(0, 0)
        self.image = pygame.image.load(IMG_DIR + "bar_keeper.png")

    def update(self, context: Context):
        for event in context.events:
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_UP and self.position.y > 0:
                self.position.y -= 1
            elif event.key == pygame.K_DOWN and self.position.y < 6:
                self.position.y += 1
            elif event.key == pygame.K_LEFT and self.position.x > 0:
                self.position.x -= 1
            elif event.key == pygame.K_RIGHT and self.position.x < 9:
                self.position.x += 1