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
    def __init__(self, x: int = 0, y: int = 0, status=CustomerStatus.WALKING):
        super().__init__()
        self.bubble = None
        self.tile_rect = Rect(x, y, 1, 1)
        # status determines if the customer is sitting or walking
        self.status = status
        self.obstacle = True
        self.happiness = None
        self.order_value = None
        self.timer = time.time()
        self.walk_timer = time.time()
        self.is_walking = True
        self.track = None
        self.volume = None
        self.temperature = None
        self.path = [Rect(1, 1, 1, 1), Rect(1, 2, 1, 1), Rect(1, 3, 1, 1), Rect(2, 3, 1, 1), Rect(3, 3, 1, 1),
                     Rect(3, 4, 1, 1), Rect(4, 4, 1, 1), Rect(5, 4, 1, 1)]

        self.register_surface(
            "image",
            lambda: pygame.image.load(IMG_DIR + "dummy.png")
        )

    @property
    def image(self) -> Surface:
        return self.get_surface("image")

    def get_order_value(self):
        return self.order_value

    def customer_walking(self, context: Context):
        for i in self.path:
            for sprite in context.current_room.sprites:
                if sprite is self:
                    break
                if type(sprite) == type(self):
                    if sprite.is_near(self):
                        self.is_walking = False
                    else:
                        self.is_walking = True

            if time.time() - self.walk_timer > 20/60 and self.is_walking:
                self.tile_rect = i
                self.walk_timer = time.time()
                self.path.pop(0)

    def generate_order_walking(self):
        # generate order for walkers from random value
        if self.status == CustomerStatus.WALKING and self.order_value is None:
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
        else:
            pass

    def generate_order_sitting(self):
        if self.status == CustomerStatus.SITTING:
            if self.order_value is None and time.time() - self.timer >= 40:
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

    # Display the customers order
    def display_order(self, context: Context):
        if not self.bubble:
            self.bubble = SpeechBubble(self)
            if self.status == CustomerStatus.WALKING:
                self.bubble.content = OrderWalkersContent(self.order_value)
            elif self.order_value == OrderSitters.CHANGE_MUSIC:
                self.bubble.content = OrderSittersContent(self.order_value)
                self.track = context.rooms["bar"].track
                pass
            elif self.order_value == OrderSitters.MUSIC_VOLUME_UP:
                self.volume = context.rooms["bar"].volume
                self.bubble.content = OrderSittersContent(self.order_value)
                pass
            elif self.order_value == OrderSitters.MUSIC_VOLUME_DOWN:
                self.volume = context.rooms["bar"].volume
                self.bubble.content = OrderSittersContent(self.order_value)
                pass
            elif self.order_value == OrderSitters.TEMPERATURE_UP:
                self.temperature = context.rooms["bar"].temperature
                self.bubble.content = OrderSittersContent(self.order_value)
                pass
            elif self.order_value == OrderSitters.TEMPERATURE_DOWN:
                self.temperature = context.rooms["bar"].temperature
                self.bubble.content = OrderSittersContent(self.order_value)
                pass
        context.current_room.bubbles.append(self.bubble)
        self.timer = time.time()

    def check_order_walkers(self, context: Context):
        # TODO: Check and Adjust times
        self.timer = time.time() - self.timer
        # Check if correct order was served in what time
        for sprite in context.current_room.sprites:
            if type(sprite) == BarKeeper:
                if sprite.item == self.order_value and self.timer < 20:
                    self.happiness = CustomerHappiness.HAPPY
                    # TODO: HIGHSCORE and leave
                elif sprite.item == self.order_value and 20 <= self.timer < 40:
                    self.happiness = CustomerHappiness.NEUTRAL
                    # TODO: HIGHSCORE and leave
                elif sprite.item == self.order_value and self.timer >= 40:
                    self.happiness = CustomerHappiness.UNHAPPY
                    # TODO: HIGHSCORE and leave
                elif sprite.item != self.order_value:
                    self.happiness = CustomerHappiness.UNHAPPY
                    # TODO: HIGHTSCORE and leave
                self.order_value = None
                sprite.item = None

    # For sitting customers
    def check_order_sitters(self, context: Context):
        # TODO: HIGHSCORE
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
            self.order_value = None
            self.timer = time.time()

    def update(self, context: Context):
        self.customer_walking(context)
        if self.tile_rect == Rect(5, 4, 1, 1) and time.time() - self.walk_timer > 20/60:
            self.display_order(context)
