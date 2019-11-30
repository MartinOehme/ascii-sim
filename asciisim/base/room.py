from typing import List

from pygame import Rect
from pygame import Surface

from .game_object import GameObject

from ..sprites.sprite_enums import MusicTracks

class Room(GameObject):
    def __init__(self):
        self.obstacles: List[SpritePosition] = []
        self.sprites = []
        self.bubbles = []
        self.sidebar_left = True
        
        # radiator temperature
        self.temperature = 22
        # music
        self.track: MusicTracks = None
        self.volume = 50

    @property
    def renderable_sprites_by_z_index(self):
        return filter(
            lambda sprite: sprite.renderable,
            sorted(self.sprites, key = lambda sprite: sprite.z_index)
        )

    
    def has_obstacle(self, other: GameObject, dx: int, dy: int) -> bool:
        tmp_tile_rect = Rect(
            other.tile_rect.left + dx,
            other.tile_rect.top + dy,
            other.tile_rect.width,
            other.tile_rect.height,
        )
        
        return -1 != tmp_tile_rect.collidelist(self.obstacles)
