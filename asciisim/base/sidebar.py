import pygame
from pygame import Rect

from .context import Context
from .game_object import GameObject
from ..res import IMG_DIR

class SideBar(GameObject):
    def __init__(self):
        self.is_left = True
        self.register_surface(
            "sidebar",
            lambda: pygame.image.load(IMG_DIR + "sidebar.png")
        )
        
    @property
    def image(self):
        return self.get_surface("sidebar")
        
    def update(self, context):
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
