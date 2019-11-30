import time

import pygame
from pygame import Rect

from .bar_keeper import BarKeeper
from .sprite_enums import MachineStates
from .sprite_enums import CoffeeTypes
from ..base.sprite import AbstractSprite
from ..base.context import Context
from ..base.closeup import Closeup
from ..base.speech_bubble import SpeechBubble
from ..menu.control import Control
from ..menu.menu import Menu
from ..res import IMG_DIR
from ..speech_bubble.machine_states import MachineStatesContent

class CoffeeMachineCloseup(Closeup):
    def __init__(self, coffee_machine: 'CoffeeMachine'):
        super().__init__(IMG_DIR + "coffee_machine/coffee_machine_closeup.png")
        self.coffee_machine = coffee_machine
        self.menu = Menu()
        self.menu.add_control(Control(480, 30, 550, 210))
        self.menu.add_control(Control(460, 650, 300, 100))
        self.menu.add_control(Control(850, 630, 220, 100))
        self.menu.add_control(Control(470, 770, 520, 130))
        self.menu.add_control(Control(50, 630, 300, 350))
        self.menu.add_control(Control(1470, 600, 200, 200))
        
        self.sprites += self.menu.control_sprites
        
    def update(self, context: Context) -> None:
        self.menu.update(context)
        for event in context.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                context.closeup = None
                self.coffee_machine.state = MachineStates.NOT_USED
        
class CoffeeMachine(AbstractSprite):
    def __init__(self):
        super().__init__()
        self.tile_rect = Rect(9, 3, 1, 2)
        self.renderable = False
        self._state = MachineStates.NOT_USED
        self.broken_status = list()
        self.broken_status.append(MachineStates.ALL_GOOD)
        self.status_displayed = False
        self.obstacle = True
        
        self.pot = False
        self.coffee_grounds = 0
        self.sewage = 0
        self.milk: int = 10
        self.coffee: int = 50

        self.closeup = CoffeeMachineCloseup(self)
        self.last_coffee: CoffeeTypes = None
        self.coffee_time = time.time()

        self.bubble = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value


    def update(self, context: Context):
        if not self.bubble:
            self.bubble = SpeechBubble(self)
            self.bubble.content = MachineStatesContent(self.state)
            context.current_room.bubbles.append(self.bubble)

        for event in context.events:
            if (
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_q)
            ):
                for sprite in context.current_room.sprites:
                    if type(sprite) == BarKeeper:
                        if sprite.is_near(self):
                            self.state = MachineStates.IN_USE

        if self.state is MachineStates.IN_USE:
            # What to do generally:
            # - open interface
            context.closeup = self.closeup
