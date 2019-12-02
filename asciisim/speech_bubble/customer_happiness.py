import pygame

from asciisim.res import IMG_DIR
from ..base.content import Content
from ..sprites.sprite_enums import CustomerHappiness


class CustomerHappinessContent(Content):
    def __init__(self, state: CustomerHappiness):
        super().__init__()
        self.state = state
        self.register_surface(
            f"image_{self.state.value}",
            lambda: pygame.image.load(IMG_DIR + "speech_bubbles/customer_happiness/" + state.value + ".png")
        )

    @property
    def image(self) -> pygame.Surface:
        return self.get_surface(f"image_{self.state.value}")
