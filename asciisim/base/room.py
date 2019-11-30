from typing import List

from pygame import Surface

from .sprite_position import SpritePosition

class Room(object):
    def __init__(self):
        self.background: Surface = None
        self.obstacles: List[SpritePosition] = []
        self.sprites = []

    def has_obstacle(self, x: int, y: int) -> bool:
        return bool(
            [pos for pos in self.obstacles
             if pos.x == x and pos.y == y]
        )
