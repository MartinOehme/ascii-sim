import pygame

from pygame.rect import Rect

from asciisim.res import IMG_DIR
from asciisim.sprites.sprite_enums import MachineStates
from ..base.closeup import Closeup
from ..base.context import Context
from ..base.sprite import AbstractSprite
from ..menu.control import Control
from ..menu.menu import Menu
from ..sprites.bar_keeper import BarKeeper


class CoffeeStorageCloseup(Closeup):
    def __init__(self, coffee_storage: 'CoffeeStorage'):
        super().__init__(IMG_DIR + "coffee_storage/coffee_storage_closeup.png")
        self.coffee_storage = coffee_storage
        self.menu = Menu()
        self.menu.add_control(Control(760, 400, 400, 100))

        self.sprites += self.menu.control_sprites

    def update(self, context: Context) -> None:
        self.menu.update(context)
        for event in context.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.menu.control_index == 0:
                    self.coffee_storage.state = MachineStates.REFILL_COFFEE

                context.closeup = None

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                context.closeup = None


class CoffeeStorage(AbstractSprite):
    def __init__(self):
        super().__init__()
        self.closeup = CoffeeStorageCloseup(self)
        self.tile_rect = Rect(0, 3, 2, 1)
        self.obstacle = True
        self.renderable = False
        self.state = None

    def update(self, context: Context):
        for event in context.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                for sprite in context.current_room.sprites:
                    if type(sprite) == BarKeeper:
                        if sprite.is_near(self):
                            sprite.item = self.state
                            context.closeup = self.closeup
