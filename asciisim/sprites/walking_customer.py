import random
import time
from typing import List

import pygame
from pygame import Rect
from pygame import Surface

from .abstract_customer import AbstractCustomer
from .bar_keeper import BarKeeper
from .sprite_enums import CustomerHappiness
from .sprite_enums import CustomerStatus
from .sprite_enums import Direction
from .sprite_enums import OrderWalkers
from ..base.context import Context
from ..base.speech_bubble import SpeechBubble
from ..res import IMG_DIR
from ..speech_bubble.customer_happiness import CustomerHappinessContent
from ..speech_bubble.order_walkers import OrderWalkersContent
from ..util.debounce import Debounce


class WalkingCustomer(AbstractCustomer):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y, status=CustomerStatus.WALKING)
        self.path = [
            Rect(1, 1, 1, 1), Rect(1, 2, 1, 1), Rect(1, 3, 1, 1),
            Rect(2, 3, 1, 1), Rect(3, 3, 1, 1), Rect(3, 4, 1, 1),
            Rect(4, 4, 1, 1), Rect(5, 4, 1, 1)
        ]
        self.return_path = [
            Rect(5, 3, 1, 1), Rect(5, 2, 1, 1),
            Rect(5, 1, 1, 1), Rect(4, 1, 1, 1), Rect(3, 1, 1, 1),
            Rect(2, 1, 1, 1), Rect(1, 1, 1, 1), Rect(1, 0, 1, 1)
        ]
        self.direction = Direction.DOWN
        self.register_surface(
            Direction.UP.value,
            lambda: pygame.image.load(IMG_DIR + "customer/up.png")
        )
        self.register_surface(
            Direction.DOWN.value,
            lambda: pygame.image.load(IMG_DIR + "customer/down.png")
        )
        self.register_surface(
            Direction.RIGHT.value,
            lambda: pygame.image.load(IMG_DIR + "customer/right.png")
        )
        self.register_surface(
            Direction.LEFT.value,
            lambda: pygame.image.load(IMG_DIR + "customer/left.png")
        )
        self.time_ordered = 0

    @property
    def image(self) -> Surface:
        return self.get_ani_surface(
            self.direction.value,
            (90, 135),
            self.animation.current_frame
        )

    @Debounce(300)
    def customer_walking(self, context: Context, route: List[Rect]):
        if not route:
            return
        next_step = route[0]
        dx = next_step.left - self.tile_rect.left
        dy = next_step.top - self.tile_rect.top
        if context.current_room.has_obstacle(self, dx, dy):
            return
        self.animation.start()
        self.tile_rect = next_step
        route.pop(0)

    def generate_order(self):
        random_value = random.randint(0, 99)
        if 0 <= random_value < 12:
            self.order_value = OrderWalkers.COFFEE
        elif 12 <= random_value < 24:
            self.order_value = OrderWalkers.COFFEE_MILK
        elif 24 <= random_value < 48:
            self.order_value = OrderWalkers.RETURN_CUP
        elif 48 <= random_value < 54:
            self.order_value = OrderWalkers.KOLLE_MATE
        elif 54 <= random_value < 60:
            self.order_value = OrderWalkers.PREMIUM_COLA
        elif 60 <= random_value < 66:
            self.order_value = OrderWalkers.ZOTRINE
        elif 66 <= random_value < 72:
            self.order_value = OrderWalkers.BONBON
        elif 72 <= random_value < 96:
            self.order_value = OrderWalkers.RETURN_BOTTLE
        elif 96 <= random_value < 98:
            self.order_value = OrderWalkers.GET_BROOM
        elif 98 <= random_value <= 99:
            self.order_value = OrderWalkers.RETURN_BROOM
        self.time_ordered = time.time()

    def check_order(self, context: Context):
        if not self.bubble:
            # Do not serve customers not at the bar
            return

        order_time = time.time() - self.time_ordered
        bar_keeper: BarKeeper = context.bar_keeper
        # Check if correct order was served in what time
        if self.order_value == OrderWalkers.RETURN_BOTTLE:
            if order_time < 6:
                self.happiness = CustomerHappiness.HAPPY
            else:
                self.happiness = CustomerHappiness.NEUTRAL
            bar_keeper.item = OrderWalkers.RETURN_BOTTLE
        elif self.order_value == OrderWalkers.RETURN_CUP:
            if order_time < 6:
                self.happiness = CustomerHappiness.HAPPY
            else:
                self.happiness = CustomerHappiness.NEUTRAL
            self.happiness = CustomerHappiness.HAPPY
            bar_keeper.item = OrderWalkers.RETURN_CUP
        elif self.order_value == OrderWalkers.RETURN_BROOM:
            if order_time < 6:
                self.happiness = CustomerHappiness.HAPPY
            else:
                self.happiness = CustomerHappiness.NEUTRAL
            self.happiness = CustomerHappiness.HAPPY
            bar_keeper.item = OrderWalkers.RETURN_BROOM
        elif bar_keeper.item != self.order_value:
            self.happiness = CustomerHappiness.UNHAPPY
            bar_keeper.item = None
        elif bar_keeper.item == self.order_value:
            if order_time < 20:
                self.happiness = CustomerHappiness.HAPPY
            else:
                self.happiness = CustomerHappiness.NEUTRAL
            bar_keeper.item = None
        self.pay_barkeeper(context)
        self.order_value = None
        self.is_order_done = True
        self.path = self.return_path

    def customer_interaction(self, context: Context):
        bar_keeper: BarKeeper = context.bar_keeper
        if not bar_keeper.looks_at(self, 2):
            return
        if self.is_order_done:
            return
        for event in context.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.check_order(context)

    def display_order(self, context: Context):
        if not self.bubble:
            self.bubble = SpeechBubble(self)
            self.bubble.content = OrderWalkersContent(self.order_value)
            context.current_room.bubbles.append(self.bubble)

    def update(self, context: Context):
        self.animation.update()
        self.customer_walking(context, self.path)
        if self.tile_rect == Rect(5, 4, 1, 1) and not self.order_value:
            # The customer is a the bar and has not ordered yet
            self.generate_order()
            self.display_order(context)
        self.customer_interaction(context)

