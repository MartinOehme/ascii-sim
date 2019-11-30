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
        self.menu.add_control(Control(480, 30, 550, 210))       # 0 -> Coffee tank
        self.menu.add_control(Control(460, 650, 300, 100))      # 1 -> Coffee with Milk button
        self.menu.add_control(Control(850, 630, 220, 100))      # 2 -> Coffee button
        self.menu.add_control(Control(470, 770, 520, 130))      # 3 -> Coffee dregs
        self.menu.add_control(Control(50, 630, 300, 350))       # 4 -> Milk tank

        self.sprites += self.menu.control_sprites
        
    def update(self, context: Context) -> None:
        self.menu.update(context)
        check_list = self.check_status()
        print(check_list)
        for status in check_list:
            if status is MachineStates.BLOCKED:
                context.closeup = None
            elif status is MachineStates.ALL_GOOD:
                check_list = self.default_routine(context, check_list)
                for event in context.events:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        if self.menu.control_index == 1:
                            self.make_coffee(CoffeeTypes.COFFEE_MILK)
                        elif self.menu.control_index == 2:
                            self.make_coffee()
            elif status is MachineStates.CLEAR_COFFEE:
                check_list = self.default_routine(context, check_list)
            elif status is MachineStates.REFILL_MILK:
                check_list = self.default_routine(context, check_list)
            elif status is MachineStates.REFILL_COFFEE:
                check_list = self.default_routine(context, check_list)

    def check_status(self):
        return_list = [MachineStates.ALL_GOOD]
        if self.coffee_machine.milk <= 0:
            try:
                return_list.remove(MachineStates.ALL_GOOD)
            except:
                pass
            return_list.append(MachineStates.REFILL_MILK)
        if self.coffee_machine.coffee <= 0:
            try:
                return_list.remove(MachineStates.ALL_GOOD)
            except:
                pass
            return_list.append(MachineStates.REFILL_COFFEE)
        if self.coffee_machine.coffee_grounds >= 20:
            try:
                return_list.remove(MachineStates.ALL_GOOD)
            except:
                pass
            return_list.append(MachineStates.CLEAR_COFFEE)
        if time.time() - self.coffee_machine.coffee_time < 5:
            try:
                return_list.remove(MachineStates.BLOCKED)
                return_list.append(MachineStates.BLOCKED)
            except:
                return_list.append(MachineStates.BLOCKED)
        else:
            try:
                return_list.remove(MachineStates.BLOCKED)
            except:
                pass

        return return_list

    def default_routine(self, context: Context, check_list: list):
        for event in context.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                context.closeup = None
                self.coffee_machine.state = MachineStates.NOT_USED
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.menu.control_index == 0:
                    try:
                        check_list.remove(MachineStates.REFILL_COFFEE)
                        self.refill_coffee()
                    except:
                        pass
                elif self.menu.control_index == 3:
                    try:
                        check_list.remove(MachineStates.CLEAR_COFFEE)
                        self.clear_dregs()
                    except:
                        pass
                elif self.menu.control_index == 4:
                    try:
                        check_list.remove(MachineStates.REFILL_MILK)
                        self.refill_milk()
                    except:
                        pass
        if len(check_list) == 0:
            check_list.append(MachineStates.ALL_GOOD)
        return check_list

    def refill_coffee(self):
        self.coffee_machine.coffee = 50

    def make_coffee(self, coffee_type: CoffeeTypes = CoffeeTypes.NORMAL_COFFEE):
        self.coffee_machine.coffee -= 1
        self.coffee_machine.coffee_grounds += 1
        if coffee_type is CoffeeTypes.COFFEE_MILK:
            self.coffee_machine.milk -= 1

        self.coffee_machine.last_coffee = coffee_type
        self.coffee_machine.coffee_time = time.time()

    def clear_dregs(self):
        self.coffee_machine.coffee_grounds = 0

    def refill_milk(self):
        self.coffee_machine.milk = 10


class CoffeeMachine(AbstractSprite):
    def __init__(self):
        super().__init__()
        self.tile_rect = Rect(9, 3, 1, 2)
        self.renderable = False
        self._state = MachineStates.NOT_USED
        self.obstacle = True
        
        self.pot = False
        self.coffee_grounds = 0
        self.milk: int = 10
        self.coffee: int = 50
        self.last_coffee: CoffeeTypes = None
        self.coffee_time = time.time()

        self.closeup = CoffeeMachineCloseup(self)

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

        if self.state is not MachineStates.BLOCKED:
            for event in context.events:
                if (
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN)
                    and (self.state is not MachineStates.COFFEE_READY)
                ):
                    for sprite in context.current_room.sprites:
                        if type(sprite) == BarKeeper:
                            if sprite.is_near(self):
                                context.closeup = self.closeup
                if (
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN)
                    and (self.state is MachineStates.COFFEE_READY)
                ):
                    # TODO: Return coffee to barkeeper
                    pass
