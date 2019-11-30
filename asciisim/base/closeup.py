import pygame
from pygame import Rect
from pygame import Surface

from .game_object import GameObject

class Closeup(GameObject):
    def __init__(self, background_path):
        self.register_surface(
            "background",
            lambda: pygame.image.load(background_path)
        )
        self.menu = None
        self.sprites = []

    @property
    def rect(self) -> Rect:
        scale = self.TILE_SIZE / 135
        return Rect(
            0, 0,
            1920 * scale,
            1080 * scale
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
