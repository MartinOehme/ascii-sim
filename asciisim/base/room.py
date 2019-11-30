from typing import List

from pygame import Surface

from .game_object import GameObject
from .sprite_position import SpritePosition


class Room(GameObject):
    def __init__(self):
        self.obstacles: List[SpritePosition] = []
        self.sprites = []
        self.bubbles = []

        # radiator temperature
        self.temperature = 22
        # music volume
        self.volume = 50

    @property
    def sprites_by_z_index(self):
        return sorted(self.sprites, key = lambda sprite: sprite.z_index)
        
    def has_obstacle(self, x: int, y: int) -> bool:
        return bool(
            [pos for pos in self.obstacles
             if pos.x == x and pos.y == y]
        )
