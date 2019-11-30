import pygame
from pygame import Surface

from .game_object import GameObject

class Closeup(GameObject):
    def __init__(self, background_path):
        self.register_surface(
            "background",
            lambda: pygame.image.load(background_path)
        )
        self.sprites = []

    @property
    def background(self) -> Surface:
        return self.get_surface("background")

    def update(self, context) -> None:
        pass
