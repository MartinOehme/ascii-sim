import pygame
from pygame import Rect
from pygame import Surface

from ..base.sprite import AbstractSprite
from ..base.context import Context
from .sprite_enums import MachineStates


class StaticSprite(AbstractSprite):
    def __init__(self, tile_rect: Rect, image_path: str):
        super().__init__()
        self.tile_rect = tile_rect
        self.register_surface(
            "image",
            lambda: pygame.image.load(image_path)
        )
        self.state: MachineStates = MachineStates.NOT_USED

    @property
    def image(self) -> Surface:
        return self.get_surface("image")

    def update(self, context: Context):
        pass

    def use_sprite(self):
        pass
