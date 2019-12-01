import pygame
from pygame import Rect
from pygame import Surface
import time

from ..base.sprite import AbstractSprite
from ..base.context import Context
from ..res import IMG_DIR
from ..util.debounce import Debounce

debounce_decorator = Debounce(300)


class BarKeeper(AbstractSprite):
    WALK_ANIM_FRAME = 75
    WALK_ANIM_FRAME_COUNT = 4
    WALK_ANIM_DURATION = 300
    
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__()
        self.tile_rect = Rect(x, y, 1, 1) 
        self.item = None
        self.direction = "down"
        self.frame = 0
        self.last_frame = 0
        self.anim_started = 0
        
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

    def start_anim(self):
        ms = time.time_ns() // 1000000
        self.anim_started = ms
        self.last_frame = ms

    def continue_anim(self):
        ms = time.time_ns() // 1000000
        if ms - self.anim_started > self.WALK_ANIM_DURATION:
            return

        if ms - self.last_frame < self.WALK_ANIM_FRAME:
            return

        self.last_frame = ms

        if self.frame + 1 < self.WALK_ANIM_FRAME_COUNT:
            self.frame += 1
        else:
            self.frame = 0
        
    @property
    def image(self) -> Surface:
        return self.get_ani_surface(self.direction, (135, 135), self.frame)

    @debounce_decorator
    def move_up(self, context):
        self.direction = "up"
        self.start_anim()
        if self.tile_rect.top > 0:    
            if context.current_room.has_obstacle(self, 0, -1):
                return
            self.tile_rect.top -= 1


    @debounce_decorator
    def move_down(self, context):
        self.direction = "down"
        self.start_anim()
        if self.tile_rect.top < 6:
            if context.current_room.has_obstacle(self, 0, 1):
                return
                
            self.tile_rect.top += 1

    @debounce_decorator
    def move_left(self, context):
        self.direction = "left"
        self.start_anim()
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

    @debounce_decorator
    def move_right(self, context):
        self.direction = "right"
        self.start_anim()
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
                    
    def update(self, context):
        self.continue_anim()
        if context.keys_pressed[pygame.K_UP]:
            self.move_up(context)
        elif context.keys_pressed[pygame.K_DOWN]:
            self.move_down(context)
        elif context.keys_pressed[pygame.K_LEFT]:
            self.move_left(context)
        elif context.keys_pressed[pygame.K_RIGHT]:
            self.move_right(context)
            
        for event in context.events:
            if event.type != pygame.KEYDOWN:
                continue
            elif event.key == pygame.K_ESCAPE:
                exit()

    @property
    def rect(self):
        ms = time.time_ns() // 1000000
        rect = super().rect
        anim_progress =  (ms - self.anim_started) / self.WALK_ANIM_DURATION
        if anim_progress > 1:
            return rect
        
        if self.direction == "up":
            rect.top += self.TILE_SIZE * (1 - anim_progress) 
        elif self.direction == "down":
            rect.top -= self.TILE_SIZE * (1 - anim_progress)
        elif self.direction == "left":
            rect.left += self.TILE_SIZE * (1 - anim_progress)
        elif self.direction == "right":
            rect.left -= self.TILE_SIZE * (1 - anim_progress)
            
        return rect
