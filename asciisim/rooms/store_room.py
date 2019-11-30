import pygame
from pygame import Surface
from pygame import Rect

from asciisim.sprites.refrigerator import Refrigerator
from ..base.room import Room
from ..res import IMG_DIR
from ..sprites.bar_keeper import BarKeeper


class StoreRoom(Room):
    def __init__(self):
        super().__init__()
        self.register_surface(
            "background",
            lambda: pygame.image.load(IMG_DIR + "store_room.png")
        )

        self.sprites.append(
            BarKeeper(0, 6)
        )

        self.sprites.append(
            Refrigerator()
        )

        self.sidebar_left = False

    @property
    def background(self) -> Surface:
        return self.get_surface("background")
