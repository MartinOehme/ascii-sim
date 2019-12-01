import pygame
from pygame import Surface

from ..base.context import Context

from ..sprites.refrigerator import Refrigerator
from ..sprites.coffee_storage import CoffeeStorage
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
            Refrigerator()
        )

        self.sprites.append(
            CoffeeStorage()
        )

        self.sidebar_left = False

    @property
    def background(self) -> Surface:
        return self.get_surface("background")

    def update(self, context: Context):
        pass
