import pygame

from pygame.rect import Rect

from asciisim.res import IMG_DIR
from asciisim.sprites.sprite_enums import OrderWalkers
from ..base.closeup import Closeup
from ..base.context import Context
from ..base.sprite import AbstractSprite
from ..menu.control import Control
from ..menu.menu import Menu
from ..sprites.bar_keeper import BarKeeper


class RefrigeratorCloseup(Closeup):
    def __init__(self, refrigeratore: 'Refrigerator'):
        super().__init__(IMG_DIR + "refrigeratore/refrigeratore_closeup.png")
        self.refrigeratore = refrigeratore
        self.menu = Menu()
        self.menu.add_control(Control(250, 250, 255, 750))
        self.menu.add_control(Control(594, 250, 255, 750))
        self.menu.add_control(Control(950, 250, 255, 750))

        self.sprites += self.menu.control_sprites

    def update(self, context: Context) -> None:
        self.menu.update(context)
        for event in context.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                for sprite in context.current_room.sprites:
                    if type(sprite) == BarKeeper:
                        if self.menu.control_index == 0:
                            sprite.item = OrderWalkers.PREMIUM_COLA
                        elif self.menu.control_index == 1:
                            sprite.item = OrderWalkers.ZOTRINE
                        elif self.menu.control_index == 2:
                            sprite.item = OrderWalkers.KOLLE_MATE

                    context.closeup = None

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                context.closeup = None


class Refrigerator(AbstractSprite):
    def __init__(self):
        super().__init__()
        self.closeup = RefrigeratorCloseup(self)
        self.tile_rect = Rect(0, 4, 2, 1)
        self.obstacle = True
        self.renderable = False
        self.state = None

    def update(self, context: Context):
        for event in context.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                for sprite in context.current_room.sprites:
                    if type(sprite) == BarKeeper:
                        if sprite.looks_at(self):
                            context.closeup = self.closeup
