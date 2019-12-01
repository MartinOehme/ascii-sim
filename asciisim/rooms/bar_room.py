import pygame
from pygame import Rect
from pygame import Surface
import random
import time

from asciisim.sprites.sprite_enums import OrderSitters
from ..base.speech_bubble import SpeechBubble
from ..base.room import Room
from ..base.context import Context
from ..res import IMG_DIR
from ..sprites.bar_keeper import BarKeeper
from ..sprites.customer import CustomerSprite
from ..sprites.coffee_machine import CoffeeMachine
from ..sprites.static_sprite import StaticSprite
from ..sprites.sprite_enums import CustomerStatus

from ..sprites.sprite_enums import MusicTracks

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
        ]

        BarKeeper(9, 6)

        customer = CustomerSprite(0, 5, status=CustomerStatus.SITTING)
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
        for i, sprite in enumerate(context.current_room.sprites, start=0):
            if type(sprite) == CustomerSprite and sprite.status == CustomerStatus.WALKING:
                self.number_of_customers += 1
                if len(sprite.return_path) <= 0:
                    self.bubbles.pop(self.bubbles.index(sprite.bubble))
                    self.sprites.pop(i)
                    self.number_of_customers -= 1
        random_value = random.randint(10, 30)
        if self.number_of_customers < 5 and time.time() - self.timer > random_value:
            self.timer = time.time()
            customer = CustomerSprite(1, 0)
            self.sprites.append(
                customer
            )

