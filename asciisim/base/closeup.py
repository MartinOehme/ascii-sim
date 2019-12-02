import pygame
from pygame import Rect
from pygame import Surface

from .game_object import GameObject


class Closeup(GameObject):
    def __init__(self, background_path):
        super().__init__()
        self.register_surface(
            "background",
            lambda: pygame.image.load(background_path)
        )
        self.menu = None
        self.sprites = []

    @property
    def rect(self) -> Rect:
        return Rect(
            0, 0,
            1920 * self.SCALING,
            1080 * self.SCALING
        )

    @property
    def renderable_sprites(self):
        return filter(
            lambda sprite: sprite.renderable,
            self.sprites
        )

    @property
    def background(self) -> Surface:
        return self.get_surface("background")

    def update(self, context) -> None:
        pass
