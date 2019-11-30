import pygame
from pygame.time import Clock
from pygame import Surface

from .base.context import Context
from .render_context import RenderContext
from .rooms.bar_room import BarRoom
from .rooms.store_room import StoreRoom

class Game(object):    
    def __init__(self):
        self.clock: Clock = Clock()
        self.context: Context = Context()
        self.context.rooms[Context.BAR_ROOM] = BarRoom()
        self.context.rooms[Context.STORE_ROOM] = StoreRoom()
        self.context.set_room(Context.BAR_ROOM)
        self.render_context = RenderContext((1920, 1080))
        self.running = True
        
    def update(self):
        self.context.events = pygame.event.get()
        for event in self.context.events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.render_context.resize(event.dict['size'])
        for sprite in self.context.current_room.sprites:
            sprite.update(self.context)
        self.clock.tick(60)
                
    def render(self):
        if self.context.closeup is None:
            self.render_context.screen.blit(
                self.context.current_room.background,
                (0, 0)
            )

            for sprite in self.context.current_room.sprites:
                self.render_context.screen.blit(
                    sprite.image, sprite.position.rect
                )

            for bubble in self.context.current_room.bubbles:
                self.render_context.screen.blit(
                    bubble.image, bubble.position
                )
        else:
            self.render_context.screen.blit(
                self.context.closeup.background, (0, 0)
            )

            for sprite in self.context.closeup.sprites:
                self.render_context.screen.blit(
                    sprite.image, sprite.position.rect
                )

        pygame.display.flip()
        
    def main(self):
        while self.running:
            self.update()
            self.render()

