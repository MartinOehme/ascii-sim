from abc import ABC
from typing import Callable

import pygame
from pygame import Surface


class GameObject(ABC):
    BASE_SURFACES = {}
    SCALED_SURFACES = {}

    
    def register_surface(self, name: str, callback: Callable[[], Surface]) -> None:
        key = f"{type(self)}_{name}"

        if key in self.BASE_SURFACES:
            return

        self.BASE_SURFACES[key] = callback()
        self.SCALED_SURFACES[key] = self.BASE_SURFACES[key]

    @classmethod
    def update_render_context(cls, render_context) -> None:
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
