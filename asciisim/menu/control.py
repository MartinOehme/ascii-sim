import pygame
from pygame import Rect
from pygame import Surface

from ..base.game_object import GameObject

class Control(GameObject):
    SCALING = 1
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__()
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.register_surface(
            f"active_{width}_{height}",
            self.create_active_surface
        )
        self.register_surface(
            f"passive_{width}_{height}",
            self.create_passive_surface
        )
        self.selected = False
        
    def create_active_surface(self):
        surface = Surface(self.rect.size, flags = pygame.SRCALPHA)
        pygame.draw.rect(
            surface, (255, 255, 255),
            Rect(0, 0, self.width, self.height), 20
        )

        return surface

    def create_passive_surface(self):
        surface = Surface(self.rect.size, flags = pygame.SRCALPHA)
        pygame.draw.rect(
            surface, (100, 100, 100),
            Rect(0, 0, self.width, self.height), 20
        )

        return surface
    
    @property
    def image(self) -> Surface:
        if self.selected:
            return self.get_surface(f"active_{self.width}_{self.height}")

        return self.get_surface(f"passive_{self.width}_{self.height}")
        
    @property
    def rect(self) -> Rect:
        return Rect(
            self.x * self.SCALING,
            self.y * self.SCALING,
            self.width * self.SCALING,
            self.height * self.SCALING
        )

    @classmethod
    def update_render_context(cls, render_context) -> None:
        cls.SCALING = render_context.scaling

