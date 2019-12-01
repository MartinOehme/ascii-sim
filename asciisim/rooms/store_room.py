import pygame

from pygame import Surface
from pygame import Rect

from ..sprites.item import Item
from ..base.context import Context

from ..sprites.refrigerator import Refrigerator
from ..base.room import Room
from ..res import IMG_DIR
from ..sprites.sprite_enums import OrderWalkers, MachineStates


class StoreRoom(Room):
    def __init__(self):
        super().__init__()
        self.register_surface(
            "background",
            lambda: pygame.image.load(IMG_DIR + "store_room.png")
        )

        self.obstacles += [
            Rect(4, 1, 2, 3),
            Rect(5, 4, 1, 3)
        ]

        self.sprites.append(
            Item(1, 6, 1, 1, OrderWalkers.BONBON)
        )

        self.sprites.append(
            Item(2, 6, 1, 1, MachineStates.REFILL_MILK)
        )

        self.sprites.append(
            Item(3, 6, 1, 1, OrderWalkers.GET_BROOM)
        )

        self.sprites.append(
            Item(0, 3, 2, 1, MachineStates.REFILL_COFFEE)
        )

        self.sprites.append(
            Refrigerator()
        )

        self.sidebar_left = False

    @property
    def background(self) -> Surface:
        return self.get_surface("background")

    def update(self, context: Context):
        pass
