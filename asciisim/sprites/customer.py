from pygame import Surface
from ..base.sprite import AbstractSprite
from ..base.context import Context
from ..base.sprite_position import SpritePosition
from .sprite_enums import CustomerStatus, OrderWalkers, OrderSitters
import random


class CustomerSprite(AbstractSprite):
    def __init__(self, position: SpritePosition, image: Surface):
        super().__init__()
        self.position = position
        self.image = image
        # status determines if the customer is sitting or walking
        self.status = CustomerStatus.WALKING
        self.happiness = None
        self.order_value = None

    def get_order_value(self): return self.order_value

    def generate_order(self):
        # generate order from random value
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
    def display_order(self):
        # TODO: Start timer
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
            pass
        elif self.order_value == OrderSitters.MUSIC_VOLUME_UP:
            # TODO: Display volume up dialog
            pass
        elif self.order_value == OrderSitters.MUSIC_VOLUME_DOWN:
            # TODO: Display volume down dialog
            pass
        elif self.order_value == OrderSitters.TEMPERATURE_UP:
            # TODO: Display temperature up dialog
            pass
        elif self.order_value == OrderSitters.TEMPERATURE_DOWN:
            # TODO: Display temperature down dialog
            pass

    def check_order(self):
        # TODO: End Timer
        # If barkeeper_order == order_value and fastest timer -> happy
        # If barkeeper_order == order_value and middle timer -> neutral
        # If barkeeper_order == order_value and slowest timer -> unhappy
        # If barkeeper_order != order_value -> unhappy
        pass

    def update(self, context: Context):
        pass
