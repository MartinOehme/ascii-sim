import pygame
from pygame.time import Clock
from pygame import Surface

from .base.context import Context

class Game(object):
    def __init__(self, screen):
        self.clock: Clock = Clock()
        self.context: Context = Context()
        self.running = True
        self.screen: Surface = screen
        
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        self.clock.tick(60)
                
    def render(self):
        self.screen.fill((255, 255, 255))
        pygame.display.flip()
        
    def main(self):
        while self.running:
            self.update()
            self.render()

