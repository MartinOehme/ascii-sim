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
        self.order_value = None

    def generate_order(self, status):
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
            # ------------IMPLEMENTIERUNGSIDEE-----------------
            if 0 <= random_value < 20:
                self.order_value = OrderSitters.CHANGE_MUSIC
                BarRoom.set_music_vol(3)
            elif 20 <= random_value < 40 and BarRoom.get_music_vol():
                self.order_value = OrderSitters.MUSIC_VOLUME_DOWN

    def spawn(self, context: Context):
        # TODO: Spawn in der Tür; Generation von Wünschen
        pass

    def update(self, context: Context):
        pass
