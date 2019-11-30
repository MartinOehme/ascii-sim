import pygame
from pygame import Rect
from pygame import Surface

from asciisim.base.speech_bubble import SpeechBubble
from asciisim.speech_bubble.order_sitters import OrderSittersContent
from asciisim.speech_bubble.order_walkers import OrderWalkersContent
from ..base.sprite import AbstractSprite
from ..base.context import Context
from ..res import IMG_DIR
from .sprite_enums import CustomerStatus, CustomerHappiness, OrderWalkers, OrderSitters
from .bar_keeper import BarKeeper
import random
import time


class CustomerSprite(AbstractSprite):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__()
        self.bubble = None
        self.tile_rect = Rect(x, y, 1, 1)
        # status determines if the customer is sitting or walking
        self.status = CustomerStatus.WALKING
        self.happiness = None
        self.order_value = None
        self.timer = None
        self.track = None
        self.volume = None
        self.temperature = None

        self.register_surface(
            "image",
            lambda: pygame.image.load(IMG_DIR + "dummy.png")
        )

    @property
    def image(self) -> Surface:
        return self.get_surface("image")

    def get_order_value(self):
        return self.order_value

    def generate_order(self):
        # generate order for walkers from random value
        if self.status == CustomerStatus.WALKING:
            random_value = random.randint(0, 99)
            if 0 <= random_value < 12:
                self.order_value = OrderWalkers.COFFEE
            elif 12 <= random_value < 24:
                self.order_value = OrderWalkers.COFFEE_MILK
            elif 24 <= random_value < 48:
                self.order_value = OrderWalkers.RETURN_CUP
            elif 48 <= random_value < 56:
                self.order_value = OrderWalkers.KOLLE_MATE
            elif 56 <= random_value < 64:
                self.order_value = OrderWalkers.PREMIUM_COLA
            elif 64 <= random_value < 72:
                self.order_value = OrderWalkers.ZOTRINE
            elif 72 <= random_value < 96:
                self.order_value = OrderWalkers.RETURN_BOTTLE
            elif 96 <= random_value <= 99:
                self.order_value = OrderWalkers.GET_BROOM
                # TODO: make broom return order if broom has been taken
        # generate order for sitters from random value
        elif self.status == CustomerStatus.SITTING:
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

    # spawn new customer
    def spawn(self, context: Context):
        # TODO: Spawn in der Tür;
        self.generate_order()
        pass

    # Display the customers order
    def display_order(self, context: Context):
        if self.order_value == OrderWalkers.COFFEE:
            # TODO: Display Coffee dialog
            pass
        elif self.order_value == OrderWalkers.COFFEE_MILK:
            # TODO: Display Coffee and milk dialog
            pass
        elif self.order_value == OrderWalkers.KOLLE_MATE:
            # TODO: Display mate dialog
            pass
        elif self.order_value == OrderWalkers.PREMIUM_COLA:
            # TODO: Display cola dialog
            pass
        elif self.order_value == OrderWalkers.ZOTRINE:
            # TODO: Display zotrine dialog
            pass
        elif self.order_value == OrderWalkers.RETURN_CUP:
            # TODO: Display return cup dialog
            pass
        elif self.order_value == OrderWalkers.GET_BROOM:
            # TODO: Display get broom dialog
            pass
        elif self.order_value == OrderWalkers.RETURN_BOTTLE:
            # TODO: Display return bottle dialog
            pass
        elif self.order_value == OrderWalkers.RETURN_BROOM:
            # TODO: Display return broom dialog
            pass
        elif self.order_value == OrderSitters.CHANGE_MUSIC:
            # TODO: Display change music dialog
            self.track = context.rooms["bar"].track
            pass
        elif self.order_value == OrderSitters.MUSIC_VOLUME_UP:
            self.volume = context.rooms["bar"].volume
            # TODO: Display volume up dialog
            pass
        elif self.order_value == OrderSitters.MUSIC_VOLUME_DOWN:
            self.volume = context.rooms["bar"].volume
            # TODO: Display volume down dialog
            pass
        elif self.order_value == OrderSitters.TEMPERATURE_UP:
            self.temperature = context.rooms["bar"].temperature
            # TODO: Display temperature up dialog
            pass
        elif self.order_value == OrderSitters.TEMPERATURE_DOWN:
            self.temperature = context.rooms["bar"].temperature
            # TODO: Display temperature down dialog
            pass
        self.timer = time.time()

    def check_order_walkers(self):
        # TODO: Check and Adjust times
        # TODO: Let customer leave after getting his order
        # TODO: get number of sitting customers
        self.timer = time.time() - self.timer
        # Check if correct order was served in what time
        if BarKeeper.get_current_order() == self.order_value and self.timer < 20:
            self.happiness = CustomerHappiness.HAPPY
            # Customer has a chance to sit down when served happily (50%)
            random_value = random.randint(0, 3)
            if random_value < 2:
                self.status = CustomerStatus.SITTING
                # TODO: Let customer walk to bench and sit down
        elif BarKeeper.get_current_order() == self.order_value and 20 < self.timer < 40:
            self.happiness = CustomerHappiness.NEUTRAL
            # Customer has a chance to sit down when served (25%)
            random_value = random.randint(0, 3)
            if random_value < 1:
                self.status = CustomerStatus.SITTING
                # TODO: Let customer walk to bench and sit down
        elif BarKeeper.get_current_order() == self.order_value and self.timer >= 40:
            self.happiness = CustomerHappiness.UNHAPPY
        elif BarKeeper.get_current_order() != self.order_value:
            self.happiness = CustomerHappiness.UNHAPPY

    # For sitting customers, TODO: check order after certain time
    def check_order_sitters(self, context: Context):
        self.timer = time.time() - self.timer
        # TODO
        if self.order_value == OrderSitters.CHANGE_MUSIC and self.track != context.rooms["bar"].track:
            self.track = context.rooms["bar"].track
            self.happiness = CustomerHappiness.HAPPY
        elif self.order_value == OrderSitters.CHANGE_MUSIC and self.track == context.rooms["bar"].track:
            self.track = context.rooms["bar"].track
            self.happiness = CustomerHappiness.UNHAPPY
            self.status = CustomerStatus.WALKING # TODO: Customer leaves
        elif self.order_value == OrderSitters.MUSIC_VOLUME_UP and self.volume < context.rooms["bar"].volume:
            self.volume = context.rooms["bar"].volume
            self.happiness = CustomerHappiness.HAPPY
        elif self.order_value == OrderSitters.MUSIC_VOLUME_UP and self.volume >= context.rooms["bar"].volume:
            self.volume = context.rooms["bar"].volume
            self.happiness = CustomerHappiness.UNHAPPY
            self.status = CustomerStatus.WALKING # TODO: Customer leaves
        elif self.order_value == OrderSitters.MUSIC_VOLUME_DOWN and self.volume > context.rooms["bar"].volume:
            self.volume = context.rooms["bar"].volume
            self.happiness = CustomerHappiness.HAPPY
        elif self.order_value == OrderSitters.MUSIC_VOLUME_DOWN and self.volume <= context.rooms["bar"].volume:
            self.volume = context.rooms["bar"].volume
            self.happiness = CustomerHappiness.UNHAPPY
            self.status = CustomerStatus.WALKING # TODO: Customer leaves
        elif self.order_value == OrderSitters.TEMPERATURE_UP and self.temperature < context.rooms["bar"].temperature:
            self.temperature = context.rooms["bar"].temperature
            self.happiness = CustomerHappiness.HAPPY
        elif self.order_value == OrderSitters.TEMPERATURE_UP and self.temperature >= context.rooms["bar"].temperature:
            self.temperature = context.rooms["bar"].temperature
            self.happiness = CustomerHappiness.UNHAPPY
            self.status = CustomerStatus.WALKING # TODO: Customer leaves
        elif self.order_value == OrderSitters.TEMPERATURE_DOWN and self.temperature > context.rooms["bar"].temperature:
            self.temperature = context.rooms["bar"].temperature
            self.happiness = CustomerHappiness.HAPPY
        elif self.order_value == OrderSitters.TEMPERATURE_DOWN and self.temperature <= context.rooms["bar"].temperature:
            self.temperature = context.rooms["bar"].temperature
            self.happiness = CustomerHappiness.UNHAPPY
            self.status = CustomerStatus.WALKING # TODO: Customer leaves

    def update(self, context: Context):
        if not self.bubble:
            self.bubble = SpeechBubble(self)
            if self.status == CustomerStatus.WALKING:
                self.bubble.content = OrderWalkersContent(self.order_value)
            elif self.status == CustomerStatus.SITTING:
                self.bubble.content = OrderSittersContent(self.order_value)

            context.current_room.bubbles.append(self.bubble)
