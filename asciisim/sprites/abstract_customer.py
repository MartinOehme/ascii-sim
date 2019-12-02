from abc import ABC

from pygame import Rect

from .bar_keeper import BarKeeper
from .sprite_enums import CustomerHappiness
from .sprite_enums import CustomerStatus
from ..base.context import Context
from ..base.sprite import AbstractSprite
from ..speech_bubble.customer_happiness import CustomerHappinessContent
from ..util.animation import Animation


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
        self.is_order_done = False

    def get_order_value(self):
        return self.order_value

    def pay_barkeeper(self, context: Context):
        bar_keeper: BarKeeper = context.bar_keeper
        if self.happiness == CustomerHappiness.HAPPY:
            bar_keeper.earnings += 100
        elif self.happiness == CustomerHappiness.NEUTRAL:
            bar_keeper.earnings += 50
        elif self.happiness == CustomerHappiness.UNHAPPY:
            bar_keeper.earnings -= 10

        self.bubble.content = CustomerHappinessContent(
            self.happiness
        )