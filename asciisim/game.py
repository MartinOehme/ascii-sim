import pygame
from pygame.time import Clock
from pygame import Surface

from .base.context import Context
from .rooms.bar_room import BarRoom

class Game(object):
    def __init__(self, screen):
        self.bar_room = BarRoom()
        self.clock: Clock = Clock()
        self.context: Context = Context()
        self.context.room = self.bar_room
        self.running = True
        self.screen: Surface = screen
        
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        self.clock.tick(60)
                
    def render(self):
        self.screen.blit(self.context.room.background, (0, 0))
        pygame.display.flip()
        
    def main(self):
        while self.running:
            self.update()
            self.render()

