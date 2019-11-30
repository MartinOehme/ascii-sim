import pygame

from asciisim.res import IMG_DIR
from ..base.content import Content
from ..sprites.sprite_enums import CoffeeStates


class CoffeeStatesContent(Content):
    def __init__(self, content: CoffeeStates):
        super().__init__()
        self.content = content
        self.register_surface(
            "image",
            lambda : pygame.image.load(IMG_DIR + "coffeestate/" + content + ".png")
        )

    @property
    def image(self) -> pygame.Surface:
        return self.get_surface("image")