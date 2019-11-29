import pygame
from pygame import Surface

from ..base.room import Room
from ..base.sprite_position import SpritePosition
from ..res import IMG_DIR
from ..sprites.bar_keeper import BarKeeper
from ..sprites.static_sprite import StaticSprite


class BarRoom(Room):
    def __init__(self):
        super().__init__()
        self.background: Surface = pygame.image.load(IMG_DIR + "bar_room.png")
        self.sprites.append(
            StaticSprite(
                SpritePosition(0, 0),
                pygame.image.load(IMG_DIR + "dummy.png")
            )
        )
        self.sprites.append(
            StaticSprite(
                SpritePosition(2, 4),
                pygame.image.load(IMG_DIR + "dummy.png")
            )
        )

        self.sprites.append(
            BarKeeper()
        )
        
