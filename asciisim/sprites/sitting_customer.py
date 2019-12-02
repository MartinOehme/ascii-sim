import random
import time

import pygame
from pygame import Surface

from .abstract_customer import AbstractCustomer
from .sprite_enums import CustomerHappiness
from .sprite_enums import CustomerStatus
from .sprite_enums import MusicTracks
from .sprite_enums import OrderSitters
from ..base.context import Context
from ..base.speech_bubble import SpeechBubble
from ..res import IMG_DIR
from ..speech_bubble.order_sitters import OrderSittersContent
from ..util.debounce import Debounce


class SittingCustomer(AbstractCustomer):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y, status=CustomerStatus.SITTING)
        self.old_temperature: int = 0
        self.old_track: MusicTracks = None
        self.old_volume: int = 0
        self.order_time = 0
        self.register_surface(
            "sitting",
            lambda: pygame.image.load(IMG_DIR + "sitting_customer.png")
        )

    @property
    def image(self) -> Surface:
        return self.get_surface("sitting")

    @Debounce(10000)
    def generate_order(self, context: Context):
        if random.choice([True, False, False]):
            # Abort with a probability of 66 percent
            return

        self.order_value = random.choice(list(OrderSitters))
        if self.order_value == OrderSitters.CHANGE_MUSIC:
            # Save the old song the customer does not want to hear anymore
            self.old_track = context.rooms["bar"].track
        elif (
                self.order_value == OrderSitters.TEMPERATURE_DOWN
                or self.order_value == OrderSitters.TEMPERATURE_UP
        ):
            # Save the temperature that is unsuitable for the customer
            self.old_temperature = context.rooms["bar"].temperature
        elif (
                self.order_value == OrderSitters.MUSIC_VOLUME_DOWN
                or self.order_value == OrderSitters.MUSIC_VOLUME_UP
        ):
            # Save the volume that is unsuitable for the customer
            self.old_volume = context.rooms["bar"].temperature
        self.order_time = time.time()

        if not self.bubble:
            self.bubble = SpeechBubble(self)
        self.bubble.content = OrderSittersContent(self.order_value)
        context.current_room.bubbles.append(self.bubble)

    def check_order(self, context: Context):
        order_done = False
        if (
                self.order_value == OrderSitters.CHANGE_MUSIC
                and self.old_track != context.rooms["bar"].track
        ):
            self.happiness = CustomerHappiness.HAPPY
            order_done = True
        elif (
                self.order_value == OrderSitters.MUSIC_VOLUME_UP
                and self.old_volume < context.rooms["bar"].volume
        ):
            self.happiness = CustomerHappiness.HAPPY
            order_done = True
        elif (
                self.order_value == OrderSitters.MUSIC_VOLUME_DOWN
                and self.old_volume > context.rooms["bar"].volume
        ):
            self.happiness = CustomerHappiness.HAPPY
            order_done = True
        elif (
                self.order_value == OrderSitters.TEMPERATURE_DOWN
                and self.old_temperature > context.rooms["bar"].temperature
        ):
            self.happiness = CustomerHappiness.HAPPY
            order_done = True
        elif (
                self.order_value == OrderSitters.TEMPERATURE_UP
                and self.old_temperature < context.rooms["bar"].temperature
        ):
            self.happiness = CustomerHappiness.HAPPY
            order_done = True

        if order_done:
            self.pay_barkeeper(context)
            self.order_value = None

    def update(self, context: Context):
        if not self.order_value:
            self.generate_order(context)
        elif time.time() - self.order_time > 15:
            self.happiness = CustomerHappiness.UNHAPPY
            self.order_value = None
            self.pay_barkeeper(context)
        else:
            self.check_order(context)
