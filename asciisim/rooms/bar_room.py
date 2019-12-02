import pygame
from pygame import Rect
from pygame import Surface
import random
import time

from ..base.room import Room
from ..base.context import Context
from ..res import IMG_DIR
from ..sprites.sitting_customer import SittingCustomer
from ..sprites.walking_customer import WalkingCustomer
from ..sprites.coffee_machine import CoffeeMachine

from ..sprites.environment import Radiator, MusicBox


class BarRoom(Room):
    def __init__(self):
        super().__init__()
        self.number_of_customers = 0
        self.timer = time.time()
        self.register_surface(
            "background",
            lambda: pygame.image.load(IMG_DIR + "bar_room.png")
        )
        self.obstacles += [
            Rect(7, 1, 3, 1),
            Rect(7, 2, 1, 4),
            Rect(6, 2, 1, 4),
            Rect(0, 4, 1, 3),
            Rect(1, 4, 2, 2),
            Rect(9, 5, 1, 1)
        ]

        customer = SittingCustomer(0, 5)
        self.sprites.append(
            customer
        )

        coffee_machine = CoffeeMachine()
        self.sprites.append(
            coffee_machine
        )

        # add radiator to bar
        radiator = Radiator()
        self.sprites.append(
            radiator
        )

        # add music box to bar
        music_box = MusicBox()
        self.sprites.append(
            music_box
        )

    @property
    def background(self) -> Surface:
        return self.get_surface("background")

    def update(self, context: Context):
        self.number_of_customers = 0
        for i, sprite in enumerate(context.current_room.sprites):
            if type(sprite) == WalkingCustomer:
                self.number_of_customers += 1
                if len(sprite.return_path) <= 0:
                    self.bubbles.pop(self.bubbles.index(sprite.bubble))
                    self.sprites.pop(i)
                    self.number_of_customers -= 1
        random_value = random.randint(10, 30)
        if self.number_of_customers < 5 and time.time() - self.timer > random_value:
            self.timer = time.time()
            customer = WalkingCustomer(1, 0)
            self.sprites.append(
                customer
            )
