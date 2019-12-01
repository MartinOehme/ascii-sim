import pygame
from pygame import Rect

from .context import Context
from .game_object import GameObject
from ..sprites.sprite_enums import OrderWalkers
from ..res import IMG_DIR

class SideBar(GameObject):
    def __init__(self):
        self.is_left = True
        self.register_surface(
            "sidebar",
            lambda: pygame.image.load(IMG_DIR + "sidebar.png")
        )
        self.item = None
        for icon in OrderWalkers:
            self.register_surface(
                icon.value,
                lambda: pygame.transform.smoothscale(
                    pygame.image.load(
                        IMG_DIR + f"speech_bubbles/order_walkers/{icon.value}.png"
                    ),
                    (300, 300)
                )
            )
        
    @property
    def image(self):
        surface = self.get_surface("sidebar").copy()
        scaling = self.TILE_SIZE / 135
        
        if self.item:
            surface.blit(
                self.get_surface(self.item.value),
                Rect(
                    67 * scaling,
                    675 * scaling,
                    300 * scaling,
                    300 * scaling
                )
            )
        
        return surface
        
    def update(self, context):
        self.item = context.bar_keeper.item
        if context.room_key == Context.BAR_ROOM:
            self.is_left = True
        else:
            self.is_left = False
        
    @property
    def rect(self) -> Rect:
        img_size = self.image.get_size()
        left = 0
        scaling = self.TILE_SIZE / 135
        if not self.is_left:
            left = 1920 * scaling - img_size[0]
        return Rect(
            (left, 0),
            img_size
        )
