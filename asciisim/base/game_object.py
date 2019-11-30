from abc import ABC
from typing import Callable

import pygame
from pygame import Rect
from pygame import Surface


class GameObject(ABC):
    BASE_SURFACES = {}
    SCALED_SURFACES = {}
    TILE_SIZE = 135
    
    def __init__(self):
        self.renderable = True
        self.tile_rect: Rect = None
        self.z_index = 0

    def is_near(self, other: 'GameObject') -> bool:
        return (
            (
                self.tile_rect.left - other.tile_rect.left < 2
                and not self.tile_rect.top - other.tile_rect.top
            ) or (
                self.tile_rect.top - other.tile_rect.op < 2
                and not self.tile_rect.left - other.tile_rect.left
            )
        )

        
    def register_surface(self, name: str, callback: Callable[[], Surface]) -> None:
        key = f"{type(self)}_{name}"

        if key in self.BASE_SURFACES:
            return

        self.BASE_SURFACES[key] = callback()
        self.SCALED_SURFACES[key] = self.BASE_SURFACES[key]

        
    @property
    def rect(self):
        return Rect(
            self.TILE_SIZE * self.tile_rect.left,
            self.TILE_SIZE * self.tile_rect.top,
            self.TILE_SIZE * self.tile_rect.width,
            self.TILE_SIZE * self.tile_rect.height,
        )
        
    @classmethod
    def update_render_context(cls, render_context) -> None:
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
