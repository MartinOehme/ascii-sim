import pygame
from pygame import Surface

from ..base.room import Room
from ..res import IMG_DIR

class BarRoom(Room):
    def __init__(self):
        super().__init__()
        self.background: Surface = pygame.image.load(IMG_DIR + "bar_room.png")
    
