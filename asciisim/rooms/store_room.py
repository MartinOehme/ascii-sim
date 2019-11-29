import pygame
from pygame import Surface

from ..base.room import Room
from ..base.sprite_position import SpritePosition
from ..res import IMG_DIR
from ..sprites.bar_keeper import BarKeeper

class StoreRoom(Room):
    def __init__(self):
        super().__init__()
        self.background: Surface = pygame.image.load(IMG_DIR + "store_room.png")
        self.sprites.append(
            BarKeeper()
        )
