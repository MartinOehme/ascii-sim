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
        if self.context.closeup:
            self.context.closeup.update(self.context)
        else:
            self.context.current_room.update(self.context)
            for sprite in self.context.current_room.sprites:
                sprite.update(self.context)
        if self.context.change_room:
            self.context.change_room = False
            self.render_context.sidebar_left = self.context.current_room.sidebar_left
        self.clock.tick(60)
                
    def render(self):
        current_room = self.context.current_room
        sprites_to_render = current_room.renderable_sprites_by_z_index
    
        self.render_context.screen.blit(
                self.context.current_room.background,
                (0, 0)
            )
        for sprite in sprites_to_render:
            self.render_context.screen.blit(
                sprite.image, sprite.rect
            )
        for bubble in self.context.current_room.bubbles:
            self.render_context.screen.blit(
                bubble.image, bubble.rect
            )

        if self.context.closeup:
            self.render_context.screen.blit(
                self.context.closeup.background,
                self.context.closeup.rect
            )
    
            for sprite in self.context.closeup.renderable_sprites:
                self.render_context.screen.blit(
                    sprite.image,
                    sprite.rect
                )

        pygame.display.flip()
        
    def main(self):
        while self.running:
            self.update()
            self.render()

