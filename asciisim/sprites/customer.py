import pygame
from pygame import Rect
from pygame import Surface

from asciisim.base.speech_bubble import SpeechBubble
from asciisim.speech_bubble.customer_happiness import CustomerHappinessContent
from asciisim.speech_bubble.order_sitters import OrderSittersContent
from asciisim.speech_bubble.order_walkers import OrderWalkersContent
from ..base.sprite import AbstractSprite
from ..base.context import Context
from ..res import IMG_DIR
from ..util.animation import Animation
from ..util.debounce import Debounce
from .sprite_enums import CustomerStatus
from .sprite_enums import CustomerHappiness
from .sprite_enums import Direction
from .sprite_enums import OrderWalkers
from .sprite_enums import OrderSitters
from .bar_keeper import BarKeeper
import random
import time


class CustomerSprite(AbstractSprite):
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
        self.path = [Rect(1, 1, 1, 1), Rect(1, 2, 1, 1), Rect(1, 3, 1, 1), Rect(2, 3, 1, 1), Rect(3, 3, 1, 1),
                     Rect(3, 4, 1, 1), Rect(4, 4, 1, 1), Rect(5, 4, 1, 1)]
        self.return_path = [Rect(5, 4, 1, 1), Rect(5, 3, 1, 1), Rect(5, 2, 1, 1), Rect(5, 1, 1, 1), Rect(4, 1, 1, 1),
                            Rect(3, 1, 1, 1), Rect(2, 1, 1, 1), Rect(1, 1, 1, 1), Rect(1, 0, 1, 1)]

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
        self.register_surface(
            "sitting",
            lambda: pygame.image.load(IMG_DIR + "sitting_customer.png")   
        )
        
    @property
    def image(self) -> Surface:
        if self.status == CustomerStatus.SITTING:
            return self.get_surface("sitting")
        
        return self.get_ani_surface(
            self.direction.value,
            (90, 135),
            self.animation.current_frame
        )


    def get_order_value(self):
        return self.order_value

    def customer_walking(self, context: Context, route):
        for i in route:
            for sprite in context.current_room.sprites:
                if sprite is self:
                    break
                if type(sprite) == type(self):
                    if sprite.is_near(self):
                        self.is_walking = False
                    else:
                        self.is_walking = True

            if time.time() - self.walk_timer > 20/60 and self.is_walking:
                self.animation.start()
                self.tile_rect = i
                self.walk_timer = time.time()
                route.pop(0)
                
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
        else:
            pass

    @Debounce(10000)
    def generate_order_sitting(self):
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
        
    def check_order_walkers(self, context: Context):
        if not self.bubble:
            # Do not serve customers not at the bar
            return
        self.timer = time.time() - self.timer
        # Check if correct order was served in what time
        for sprite in context.current_room.sprites:
            if type(sprite) == BarKeeper:
                if self.order_value == OrderWalkers.RETURN_BOTTLE and self.timer < 6:
                    self.happiness = CustomerHappiness.HAPPY
                    self.bubble.content = CustomerHappinessContent(
                        CustomerHappiness.HAPPY
                    )
                    self.is_order_done = True
                    sprite.item = OrderWalkers.RETURN_BOTTLE
                elif self.order_value == OrderWalkers.RETURN_BOTTLE and self.timer > 10:
                    self.happiness = CustomerHappiness.UNHAPPY
                    self.bubble.content = CustomerHappinessContent(
                        CustomerHappiness.UNHAPPY
                    )
                    self.is_order_done = True
                    sprite.item = OrderWalkers.RETURN_BOTTLE
                elif self.order_value == OrderWalkers.RETURN_CUP and self.timer < 6:
                    self.happiness = CustomerHappiness.HAPPY
                    self.bubble.content = CustomerHappinessContent(
                        CustomerHappiness.HAPPY
                    )
                    self.is_order_done = True
                    sprite.item = OrderWalkers.RETURN_CUP
                elif self.order_value == OrderWalkers.RETURN_CUP and self.timer > 10:
                    self.happiness = CustomerHappiness.UNHAPPY
                    self.bubble.content = CustomerHappinessContent(
                        CustomerHappiness.UNHAPPY
                    )
                    self.is_order_done = True
                    sprite.item = OrderWalkers.RETURN_CUP
                elif self.order_value == OrderWalkers.RETURN_BROOM and self.timer < 6:
                    self.happiness = CustomerHappiness.HAPPY
                    self.bubble.content = CustomerHappinessContent(
                        CustomerHappiness.HAPPY
                    )
                    self.is_order_done = True
                    sprite.item = OrderWalkers.RETURN_BROOM
                elif self.order_value == OrderWalkers.RETURN_BROOM and self.timer > 10:
                    self.happiness = CustomerHappiness.UNHAPPY
                    self.is_order_done = True
                    sprite.item = OrderWalkers.RETURN_BROOM
                elif sprite.item != self.order_value:
                    self.happiness = CustomerHappiness.UNHAPPY
                    self.bubble.content = CustomerHappinessContent(
                        CustomerHappiness.UNHAPPY
                    )
                    self.is_order_done = True
                    sprite.item = None
                elif sprite.item == self.order_value and self.timer < 20:
                    self.happiness = CustomerHappiness.HAPPY
                    self.bubble.content = CustomerHappinessContent(
                        CustomerHappiness.HAPPY
                    )
                    self.is_order_done = True
                    sprite.item = None
                elif sprite.item == self.order_value and 20 <= self.timer < 40:
                    self.happiness = CustomerHappiness.NEUTRAL
                    self.bubble.content = CustomerHappinessContent(
                        CustomerHappiness.NEUTRAL
                    )
                    self.is_order_done = True
                    sprite.item = None
                elif sprite.item == self.order_value and self.timer >= 40:
                    self.happiness = CustomerHappiness.UNHAPPY
                    self.bubble.content = CustomerHappinessContent(
                        CustomerHappiness.UNHAPPY
                    )
                    self.is_order_done = True
                    sprite.item = None
                self.pay_barkeeper(context)

    def pay_barkeeper(self, context: Context):
        for sprite in context.current_room.sprites:
            if type(sprite) == BarKeeper and self.status == CustomerStatus.WALKING:
                if self.happiness == CustomerHappiness.HAPPY:
                    sprite.earnings += 100
                elif self.happiness == CustomerHappiness.NEUTRAL:
                    sprite.earnings += 50
                elif self.happiness == CustomerHappiness.UNHAPPY:
                    sprite.earnings -= 10

    def customer_interaction(self, context: Context):
        for sprite in context.current_room.sprites:
            if type(sprite) == BarKeeper and sprite.looks_at(self, 2):
                for event in context.events:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.check_order_walkers(context)

    # For sitting customers
    def check_order_sitters(self, context: Context):
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

        if self.status is CustomerStatus.WALKING:
            self.animation.update()
            self.customer_walking(context, self.path)
            if self.tile_rect == Rect(5, 4, 1, 1) and time.time() - self.walk_timer > 20/60:
                self.generate_order_walking()
                self.display_order(context)
            self.customer_interaction(context)
            if self.is_order_done:
                self.customer_walking(context, self.return_path)
        elif self.status is CustomerStatus.SITTING:
            self.generate_order_sitting()
            self.display_order(context)
