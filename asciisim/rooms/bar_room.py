import pygame
from pygame import Rect
from pygame import Surface

from ..base.speech_bubble import SpeechBubble
from ..base.room import Room
from ..res import IMG_DIR
from ..sprites.bar_keeper import BarKeeper
from ..sprites.customer import CustomerSprite
from ..sprites.coffee_machine import CoffeeMachine
from ..sprites.static_sprite import StaticSprite


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
            Rect(9, 3, 1, 2),
            Rect(0, 4, 1, 3),
            Rect(1, 4, 2, 2),
        ]

        barkeeper = BarKeeper(9, 6)

        self.sprites.append(
            barkeeper
        )
        self.bubbles.append(
            SpeechBubble(barkeeper)
        )

        customer = CustomerSprite(8, 4)

        self.sprites.append(
            customer
        )
        self.bubbles.append(
            SpeechBubble(customer)
        )

        self.sprites.append(
            CoffeeMachine()
        )
        
    @property
    def background(self) -> Surface:
        return self.get_surface("background")
