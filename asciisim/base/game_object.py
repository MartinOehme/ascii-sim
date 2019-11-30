from abc import ABC
from typing import Callable

import pygame
from pygame import Rect
from pygame import Surface


class GameObject(ABC):
    BASE_SURFACES = {}
    SCALED_SURFACES = {}
    SIDEBAR_WIDTH = 435
    LEFT_BORDER = 68
    TOP_BORDER = 68
    TILE_SIZE = 135
    
    def __init__(self):
        self.renderable = True
        self.tile_rect: Rect = None
        self.z_index = 0

    def is_near(self, other: 'GameObject') -> bool:
        tmp_rect = Rect(
            self.tile_rect.left - 1,
            self.tile_rect.top - 1,
            self.tile_rect.width + 2,
            self.tile_rect.height + 2
        )
        return tmp_rect.colliderect(other.tile_rect)

        
    def register_surface(self, name: str, callback: Callable[[], Surface]) -> None:
        key = f"{type(self)}_{name}"

        if key in self.BASE_SURFACES:
            return

        self.BASE_SURFACES[key] = callback()
        self.SCALED_SURFACES[key] = self.BASE_SURFACES[key]

        
    @property
    def rect(self):
        return Rect(
            self.TILE_SIZE * self.tile_rect.left + self.SIDEBAR_WIDTH +
            self.LEFT_BORDER,
            self.TILE_SIZE * self.tile_rect.top + self.TOP_BORDER,
            self.TILE_SIZE * self.tile_rect.width,
            self.TILE_SIZE * self.tile_rect.height,
        )
        
    @classmethod
    def update_render_context(cls, render_context) -> None:
        cls.SIDEBAR_WIDTH = render_context.sidebar_width
        cls.LEFT_BORDER = render_context.left_border
        cls.TOP_BORDER = render_context.top_border
        cls.TILE_SIZE = render_context.tile_size

        for key, surface in cls.BASE_SURFACES.items():
            size = surface.get_size()
            new_size = (
                int(size[0] * render_context.scaling),
                int(size[1] * render_context.scaling)
            )
            cls.SCALED_SURFACES[key] = pygame.transform.smoothscale(
                surface,
                new_size
            )
        
    def get_surface(self, name: str) -> Surface:
        key = f"{type(self)}_{name}"

        return self.SCALED_SURFACES[key]
