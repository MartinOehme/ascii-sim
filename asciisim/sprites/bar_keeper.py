import pygame
from pygame import Rect
from pygame import Surface
import time

from .sprite_enums import Direction
from ..base.game_object import GameObject
from ..base.context import Context
from ..base.sprite import AbstractSprite
from ..res import IMG_DIR
from ..util.animation import Animation
from ..util.debounce import Debounce

debounce_decorator = Debounce(300)


class BarKeeper(AbstractSprite):    
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__()

        self.animation = Animation(4, 75, 300)
        self.tile_rect = Rect(x, y, 1, 1) 
        self.item = None
        self.direction = Direction.DOWN
        
        self.register_surface(
            Direction.UP.value,
            lambda: pygame.image.load(IMG_DIR + "bar_keeper/up.png")
        )
        self.register_surface(
            Direction.DOWN.value,
            lambda: pygame.image.load(IMG_DIR + "bar_keeper/down.png")
        )
        self.register_surface(
            Direction.RIGHT.value,
            lambda: pygame.image.load(IMG_DIR + "bar_keeper/right.png")
        )
        self.register_surface(
            Direction.LEFT.value,
            lambda: pygame.image.load(IMG_DIR + "bar_keeper/left.png")
        )
        
    @property
    def image(self) -> Surface:
        return self.get_ani_surface(
            self.direction.value,
            (135, 135),
            self.animation.current_frame
        )

    @debounce_decorator
    def move_up(self, context):
        self.direction = Direction.UP
        if self.tile_rect.top > 0:    
            if context.current_room.has_obstacle(self, 0, -1):
                return
            self.animation.start()
            self.tile_rect.top -= 1


    @debounce_decorator
    def move_down(self, context):
        self.direction = Direction.DOWN
        if self.tile_rect.top < 6:
            if context.current_room.has_obstacle(self, 0, 1):
                return

            self.animation.start()
            self.tile_rect.top += 1

    @debounce_decorator
    def move_left(self, context):
        self.direction = Direction.LEFT
        if (self.tile_rect.left == 0
            and self.tile_rect.top == 6
            and context.room_key == Context.STORE_ROOM):
            context.set_room(Context.BAR_ROOM)
            self.tile_rect.left = 9
            self.tile_rect.top = 6
        elif self.tile_rect.left > 0:
            if context.current_room.has_obstacle(self, -1, 0):
                return

            self.animation.start() 
            self.tile_rect.left -= 1

    @debounce_decorator
    def move_right(self, context):
        self.direction = Direction.RIGHT
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
            self.animation.start()
            self.tile_rect.left += 1
        elif (
                self.tile_rect.left < 5
                and context.room_key  == Context.STORE_ROOM
        ):
            if context.current_room.has_obstacle(self, 1, 0):
                return
            self.animation.start()
            self.tile_rect.left += 1
                    
    def update(self, context):
        print(self.item)
        self.animation.update()
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

    def looks_at(self, other: GameObject, max_dist = 0):
        orect = other.tile_rect
        myrect = self.tile_rect
        
        if self.direction == Direction.UP:
            distance = orect.bottom - myrect.top
            return (orect.left <= myrect.left <= orect.right
                    and distance <= max_dist and distance >= 0)
        if self.direction == Direction.DOWN:
            distance = myrect.bottom - orect.top
            return (orect.left <= myrect.left <= orect.right
                    and distance <= max_dist and distance >= 0)
        if self.direction == Direction.LEFT:
            distance = myrect.left - orect.right
            return (orect.top <= myrect.top <= orect.bottom
                    and distance <= max_dist and distance >= 0)
        if self.direction == Direction.RIGHT:
            distance = orect.left - myrect.right
            return (orect.top <= myrect.top <= orect.bottom
                    and distance <= max_dist and distance >= 0)

        
    @property
    def rect(self):
        ms = time.time_ns() // 1000000
        rect = super().rect
        anim_progress = self.animation.progress
        if self.direction == Direction.UP:
            rect.top += self.TILE_SIZE * (1 - anim_progress) 
        elif self.direction == Direction.DOWN:
            rect.top -= self.TILE_SIZE * (1 - anim_progress)
        elif self.direction == Direction.LEFT:
            rect.left += self.TILE_SIZE * (1 - anim_progress)
        elif self.direction == Direction.RIGHT:
            rect.left -= self.TILE_SIZE * (1 - anim_progress)
            
        return rect
