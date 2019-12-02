from abc import ABC
import time

import pygame
from pygame import Rect

from asciisim.base.speech_bubble import SpeechBubble
from asciisim.speech_bubble.order_sitters import OrderSittersContent
from asciisim.speech_bubble.order_walkers import OrderWalkersContent
from .bar_keeper import BarKeeper
from .sprite_enums import CustomerHappiness
from .sprite_enums import CustomerStatus
from .sprite_enums import OrderSitters
from ..base.context import Context
from ..util.animation import Animation
from ..base.sprite import AbstractSprite


class AbstractCustomer(AbstractSprite, ABC):
    def __init__(self, x: int = 0, y: int = 0, status=CustomerStatus.WALKING):
        super().__init__()
        self.animation = Animation(4, 150, 600)
        self.bubble = None
        self.tile_rect = Rect(x, y, 1, 1)
        # status determines if the customer is sitting or walking
        self.status = status
        self.obstacle = True
        self.happiness = CustomerHappiness.NEUTRAL
        self.order_value = None
        self.timer = time.time()
        self.walk_timer = time.time()
        self.is_walking = True
        self.track = None
        self.volume = None
        self.temperature = None
        self.is_order_done = False

    def get_order_value(self):
        return self.order_value

    # Display the customers order
    def display_order(self, context: Context):
        # A sitter without wish needs no bubble
        if self.status == CustomerStatus.SITTING and not self.order_value:
            return

        if not self.bubble:
            self.bubble = SpeechBubble(self)
            if self.status == CustomerStatus.WALKING:
                self.bubble.content = OrderWalkersContent(self.order_value)
            elif self.order_value == OrderSitters.CHANGE_MUSIC:
                self.bubble.content = OrderSittersContent(self.order_value)
                self.track = context.rooms["bar"].track
            elif self.order_value == OrderSitters.MUSIC_VOLUME_UP:

                self.volume = context.rooms["bar"].volume
                self.bubble.content = OrderSittersContent(self.order_value)
            elif self.order_value == OrderSitters.MUSIC_VOLUME_DOWN:
                self.volume = context.rooms["bar"].volume
                self.bubble.content = OrderSittersContent(self.order_value)
            elif self.order_value == OrderSitters.TEMPERATURE_UP:
                self.temperature = context.rooms["bar"].temperature
                self.bubble.content = OrderSittersContent(self.order_value)
            elif self.order_value == OrderSitters.TEMPERATURE_DOWN:
                self.temperature = context.rooms["bar"].temperature
                self.bubble.content = OrderSittersContent(self.order_value)
            context.current_room.bubbles.append(self.bubble)
        self.timer = time.time()

    def pay_barkeeper(self, context: Context):
        for sprite in context.current_room.sprites:
            if type(sprite) == BarKeeper and self.status == CustomerStatus.WALKING:
                if self.happiness == CustomerHappiness.HAPPY:
                    sprite.earnings += 100
                elif self.happiness == CustomerHappiness.NEUTRAL:
                    sprite.earnings += 50
                elif self.happiness == CustomerHappiness.UNHAPPY:
                    sprite.earnings -= 10
