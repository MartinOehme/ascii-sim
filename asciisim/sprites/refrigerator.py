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
        self.menu.add_control(Control(760, 200, 400, 100))
        self.menu.add_control(Control(760, 400, 400, 100))
        self.menu.add_control(Control(760, 600, 400, 100))

        self.sprites += self.menu.control_sprites

    def update(self, context: Context) -> None:
        self.menu.update(context)
        for event in context.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.menu.control_index == 0:
                    self.refrigeratore.state = OrderWalkers.KOLLE_MATE
                elif self.menu.control_index == 1:
                    self.refrigeratore.state = OrderWalkers.PREMIUM_COLA
                elif self.menu.control_index == 2:
                    self.refrigeratore.state = OrderWalkers.ZOTRINE

                context.closeup = None

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                context.closeup = None


class Refrigerator(AbstractSprite):
    def __init__(self):
        super().__init__()
        self.closeup = RefrigeratorCloseup(self)
        self.tile_rect = Rect(0, 2, 2, 3)
        self.obstacle = True
        self.renderable = False
        self.state = None

    def update(self, context: Context):
        for event in context.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                for sprite in context.current_room.sprites:
                    if type(sprite) == BarKeeper:
                        if sprite.is_near(self):
                            context.closeup = self.closeup

