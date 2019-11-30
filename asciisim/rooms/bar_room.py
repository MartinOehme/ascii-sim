import pygame
from pygame import Rect
from pygame import Surface

from asciisim.sprites.sprite_enums import OrderSitters
from ..base.speech_bubble import SpeechBubble
from ..base.room import Room
from ..base.context import Context
from ..res import IMG_DIR
from ..sprites.bar_keeper import BarKeeper
from ..sprites.customer import CustomerSprite
from ..sprites.coffee_machine import CoffeeMachine
from ..sprites.static_sprite import StaticSprite

from ..sprites.sprite_enums import MusicTracks

from ..sprites.environment import Radiator, MusicBox


class BarRoom(Room):
    def __init__(self):
        super().__init__()
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

        barkeeper = BarKeeper(9, 6)

        self.sprites.append(
            barkeeper
        )

        customer = CustomerSprite(1, 0)
        self.sprites.append(
            customer
        )
        customer.generate_order_walking()

        self.sprites.append(
            CoffeeMachine()
        )

        # add radiator to bar
        radiator = Radiator(Rect(3, 3, 1, 1))

        self.sprites.append(
            radiator
        )

        # add music box to bar
        music_box = MusicBox(Rect(4, 4, 1, 1))

        self.sprites.append(
            music_box
        )

    @property
    def background(self) -> Surface:
        return self.get_surface("background")
