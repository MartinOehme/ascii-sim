import random
import time

import pygame
from pygame import Surface

from .abstract_customer import AbstractCustomer
from .sprite_enums import CustomerHappiness
from .sprite_enums import CustomerStatus
from .sprite_enums import OrderSitters
from ..base.context import Context
from ..res import IMG_DIR
from ..util.debounce import Debounce


class SittingCustomer(AbstractCustomer):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y, status=CustomerStatus.SITTING)
        self.register_surface(
            "sitting",
            lambda: pygame.image.load(IMG_DIR + "sitting_customer.png")
        )

    @property
    def image(self) -> Surface:
        return self.get_surface("sitting")

    @Debounce(10000)
    def generate_order(self):
        if self.order_value:
            return

        random_value = random.randint(0, 9)
        if random_value % 2 == 0:
            random_value = random.randint(0, 99)
            if 0 <= random_value < 20:
                self.order_value = OrderSitters.CHANGE_MUSIC
            elif 20 <= random_value < 40:
                self.order_value = OrderSitters.MUSIC_VOLUME_UP
            elif 40 <= random_value < 60:
                self.order_value = OrderSitters.MUSIC_VOLUME_DOWN
            elif 60 <= random_value < 80:
                self.order_value = OrderSitters.TEMPERATURE_UP
            elif 80 <= random_value <= 99:
                self.order_value = OrderSitters.TEMPERATURE_DOWN
        else:
            self.timer = time.time()

    # For sitting customers
    def check_order(self, context: Context):
        if time.time() - self.timer >= 35:
            if self.order_value == OrderSitters.CHANGE_MUSIC \
                    and self.track != context.rooms["bar"].track:
                self.track = context.rooms["bar"].track
                self.happiness = CustomerHappiness.HAPPY
            elif self.order_value == OrderSitters.CHANGE_MUSIC \
                    and self.track == context.rooms["bar"].track:
                self.track = context.rooms["bar"].track
                self.happiness = CustomerHappiness.UNHAPPY
            elif self.order_value == OrderSitters.MUSIC_VOLUME_UP \
                    and self.volume < context.rooms["bar"].volume:
                self.volume = context.rooms["bar"].volume
                self.happiness = CustomerHappiness.HAPPY
            elif self.order_value == OrderSitters.MUSIC_VOLUME_UP \
                    and self.volume >= context.rooms["bar"].volume:
                self.volume = context.rooms["bar"].volume
                self.happiness = CustomerHappiness.UNHAPPY
            elif self.order_value == OrderSitters.MUSIC_VOLUME_DOWN \
                    and self.volume > context.rooms["bar"].volume:
                self.volume = context.rooms["bar"].volume
                self.happiness = CustomerHappiness.HAPPY
            elif self.order_value == OrderSitters.MUSIC_VOLUME_DOWN \
                    and self.volume <= context.rooms["bar"].volume:
                self.volume = context.rooms["bar"].volume
                self.happiness = CustomerHappiness.UNHAPPY
            elif self.order_value == OrderSitters.TEMPERATURE_UP \
                    and self.temperature < context.rooms["bar"].temperature:
                self.temperature = context.rooms["bar"].temperature
                self.happiness = CustomerHappiness.HAPPY
            elif self.order_value == OrderSitters.TEMPERATURE_UP \
                    and self.temperature >= context.rooms["bar"].temperature:
                self.temperature = context.rooms["bar"].temperature
                self.happiness = CustomerHappiness.UNHAPPY
            elif self.order_value == OrderSitters.TEMPERATURE_DOWN \
                    and self.temperature > context.rooms["bar"].temperature:
                self.temperature = context.rooms["bar"].temperature
                self.happiness = CustomerHappiness.HAPPY
            elif self.order_value == OrderSitters.TEMPERATURE_DOWN \
                    and self.temperature <= context.rooms["bar"].temperature:
                self.temperature = context.rooms["bar"].temperature
                self.happiness = CustomerHappiness.UNHAPPY
            self.pay_barkeeper(context)
            self.order_value = None
            self.timer = time.time()

    def update(self, context: Context):
        self.generate_order()
        self.display_order(context)
