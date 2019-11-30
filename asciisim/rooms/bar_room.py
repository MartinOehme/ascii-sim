import pygame
from pygame import Surface

from ..base.speech_bubble import SpeechBubble
from ..base.room import Room
from ..base.sprite_position import SpritePosition
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
            SpritePosition(9, 1),
            SpritePosition(8, 1),
            SpritePosition(7, 1),
            SpritePosition(7, 2),
            SpritePosition(7, 3),
            SpritePosition(7, 4),
            SpritePosition(7, 5),
            SpritePosition(6, 1),
            SpritePosition(6, 2),
            SpritePosition(6, 3),
            SpritePosition(6, 4),
            SpritePosition(6, 5),
        ]
        self.sprites.append(
            StaticSprite(
                SpritePosition(0, 0),
                IMG_DIR + "dummy.png"
            )
        )
        self.sprites.append(
            StaticSprite(
                SpritePosition(2, 4),
                IMG_DIR + "dummy.png"
            )
        )

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
