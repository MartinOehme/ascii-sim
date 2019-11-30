import pygame

from asciisim.res import IMG_DIR
from ..base.content import Content
from ..sprites.sprite_enums import OrderWalkers


class OrderWalkersContent(Content):
    def __init__(self, state: OrderWalkers):
        super().__init__()
        self.state = state
        self.register_surface(
            "image",
            lambda : pygame.image.load(IMG_DIR + "speech_bubbles/order_walkers/" + state.value + ".png")
        )

    @property
    def image(self) -> pygame.Surface:
        return self.get_surface("image")