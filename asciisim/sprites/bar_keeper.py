import pygame
from pygame import Rect
from pygame import Surface

from ..base.sprite import AbstractSprite
from ..base.context import Context
from ..res import IMG_DIR


class BarKeeper(AbstractSprite):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__()
        self.tile_rect = Rect(x, y, 1, 1) 
        self.item = None
        self.direction = "down"
        self.frame = 0
        
        self.register_surface(
            "up",
            lambda: pygame.image.load(IMG_DIR + "bar_keeper/up.png")
        )
        self.register_surface(
            "down",
            lambda: pygame.image.load(IMG_DIR + "bar_keeper/down.png")
        )
        self.register_surface(
            "right",
            lambda: pygame.image.load(IMG_DIR + "bar_keeper/right.png")
        )
        self.register_surface(
            "left",
            lambda: pygame.image.load(IMG_DIR + "bar_keeper/left.png")
        )
        
    @property
    def image(self) -> Surface:
        return self.get_ani_surface(self.direction, (135, 135), 0)

    def move_up(self, context):
        self.direction = "up"
        if self.tile_rect.top > 0:    
            if context.current_room.has_obstacle(self, 0, -1):
                return
            self.tile_rect.top -= 1


    def move_down(self, context):
        self.direction = "down"
        if self.tile_rect.top < 6:
            if context.current_room.has_obstacle(self, 0, 1):
                return
                
            self.tile_rect.top += 1

    def move_left(self, context):
        self.direction = "left"
        if (self.tile_rect.left == 0
            and self.tile_rect.top == 6
            and context.room_key == Context.STORE_ROOM):
            context.set_room(Context.BAR_ROOM)
            self.tile_rect.left = 9
            self.tile_rect.top = 6
        elif self.tile_rect.left > 0:
            if context.current_room.has_obstacle(self, -1, 0):
                return

            self.tile_rect.left -= 1

<<<<<<< HEAD
=======
    def move_right(self, context):
        self.direction = "right"

        if (self.tile_rect.left == 9
            and self.tile_rect.top == 6
            and context.room_key == Context.BAR_ROOM):
            context.set_room(Context.STORE_ROOM)
            self.tile_rect.left = 0
            self.tile_rect.top = 6
        elif (
                self.tile_rect.left < 9
                and context.room_key  == Context.BAR_ROOM
        ):
            if context.current_room.has_obstacle(self, 1, 0):
                return
            
            self.tile_rect.left += 1
        elif (
                self.tile_rect.left < 5
                and context.room_key  == Context.STORE_ROOM
        ):
            if context.current_room.has_obstacle(self, 1, 0):
                return
    
            self.tile_rect.left += 1
                    
>>>>>>> master
    def update(self, context: Context):
        print(self.item)

        for event in context.events:
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_UP:
                self.move_up(context)
            elif event.key == pygame.K_DOWN:
                self.move_down(context)
            elif event.key == pygame.K_LEFT:
                self.move_left(context)
            elif event.key == pygame.K_RIGHT:
                self.move_right(context)
            elif event.key == pygame.K_ESCAPE:
                exit()
