import pygame
from pygame.time import Clock
from pygame import Surface

from .base.context import Context
from .rooms.bar_room import BarRoom
from .rooms.store_room import StoreRoom


class Game(object):
    BAR_ROOM = "bar"
    STORE_ROOM = "store"
    
    def __init__(self, screen):
        self.clock: Clock = Clock()
        self.context: Context = Context()
        self.context.rooms[self.BAR_ROOM] = BarRoom()
        self.context.rooms[self.STORE_ROOM] = StoreRoom()
        self.context.set_room(self.BAR_ROOM)
        self.context.
        self.running = True
        self.screen: Surface = screen
        
    def update(self):
        self.context.events = pygame.event.get()
        for event in self.context.events:
            if event.type == pygame.QUIT:
                self.running = False
        for sprite in self.context.current_room.sprites:
            sprite.update(self.context)
        self.clock.tick(60)
                
    def render(self):
        if self.context.closeup is None:
            self.screen.blit(self.context.current_room.background, (0, 0))

            for sprite in self.context.current_room.sprites:
                self.screen.blit(sprite.image, sprite.position.rect)

            for bubble in self.context.current_room.bubbles:

                self.screen.blit(bubble.image, bubble.position)
        else:
            self.screen.blit(self.context.closeup.background, (0, 0))

            for sprite in self.context.closeup.sprites:
                self.screen.blit(sprite.image, sprite.position.rect)

        pygame.display.flip()
        
    def main(self):
        while self.running:
            self.update()
            self.render()

