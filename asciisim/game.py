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
        self.context.events = pygame.event.get()
        for event in self.context.events:
            if event.type == pygame.QUIT:
                self.running = False
        for sprite in self.context.room.sprites:
            sprite.update(self.context)
        self.clock.tick(60)
                
    def render(self):
        if self.context.closeup is None:
            self.screen.blit(self.context.room.background, (0, 0))

            for sprite in self.context.room.sprites:
                self.screen.blit(sprite.image, sprite.position.rect)

        else:
            self.screen.blit(self.context.closeup.background, (0, 0))

            for sprite in self.context.closeup.sprites:
                self.screen.blit(sprite.image, sprite.position.rect)

        pygame.display.flip()
        
    def main(self):
        while self.running:
            self.update()
            self.render()

