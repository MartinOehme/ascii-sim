from typing import List

from pygame import Surface

from .game_object import GameObject
from .sprite_position import SpritePosition


class Room(GameObject):
    def __init__(self):
        self.obstacles: List[SpritePosition] = []
        self.sprites = []
        self.bubbles = []
        
    def has_obstacle(self, x: int, y: int) -> bool:
        return bool(
            [pos for pos in self.obstacles
             if pos.x == x and pos.y == y]
        )
