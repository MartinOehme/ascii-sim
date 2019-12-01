import time

import pygame
from pygame import Rect

from .bar_keeper import BarKeeper
from .sprite_enums import MachineStates
from .sprite_enums import CoffeeTypes, OrderWalkers
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
        for status in check_list:
            if status is MachineStates.ALL_GOOD:
                check_list = self.default_routine(context, check_list)
                for event in context.events:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        if self.menu.control_index == 1:
                            self.make_coffee(CoffeeTypes.COFFEE_MILK)
                            context.closeup = None
                        elif self.menu.control_index == 2:
                            self.make_coffee()
                            context.closeup = None
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
            self.coffee_machine.state = MachineStates.REFILL_MILK
        if self.coffee_machine.coffee <= 0:
            try:
                return_list.remove(MachineStates.ALL_GOOD)
            except:
                pass
            return_list.append(MachineStates.REFILL_COFFEE)
            self.coffee_machine.state = MachineStates.REFILL_COFFEE
        if self.coffee_machine.coffee_grounds >= 20:
            try:
                return_list.remove(MachineStates.ALL_GOOD)
            except:
                pass
            return_list.append(MachineStates.CLEAR_COFFEE)
            self.coffee_machine.state = MachineStates.CLEAR_COFFEE

        return return_list

    def default_routine(self, context: Context, check_list: list):
        for sprite in context.current_room.sprites:
            if type(sprite) == BarKeeper:
                for event in context.events:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        context.closeup = None
                        self.coffee_machine.state = MachineStates.NOT_USED
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        if self.menu.control_index == 0:
                            if self.refill_coffee(sprite):
                                try:
                                    check_list.remove(MachineStates.REFILL_COFFEE)
                                except:
                                    pass

                        elif self.menu.control_index == 3:
                            self.clear_dregs()
                            try:
                                check_list.remove(MachineStates.CLEAR_COFFEE)
                            except:
                                pass

                        elif self.menu.control_index == 4:
                            if self.refill_milk(sprite):
                                try:
                                    check_list.remove(MachineStates.REFILL_MILK)
                                except:
                                    pass

                if len(check_list) == 0:
                    check_list.append(MachineStates.ALL_GOOD)
                return check_list

    def refill_coffee(self, barkeeper):
        if barkeeper.item is MachineStates.REFILL_COFFEE:
            self.coffee_machine.coffee = 50
            barkeeper.item = None
            return True
        return False

    def make_coffee(self, coffee_type: CoffeeTypes = CoffeeTypes.NORMAL_COFFEE):
        self.coffee_machine.coffee -= 1
        self.coffee_machine.coffee_grounds += 1
        self.coffee_machine.last_coffee = OrderWalkers.COFFEE
        if coffee_type is CoffeeTypes.COFFEE_MILK:
            self.coffee_machine.last_coffee = OrderWalkers.COFFEE_MILK
            self.coffee_machine.milk -= 1

        self.coffee_machine.coffee_time = time.time()

        self.coffee_machine.state = MachineStates.BLOCKED

    def clear_dregs(self):
        self.coffee_machine.coffee_grounds = 0

    def refill_milk(self, barkeeper):
        if barkeeper.item is MachineStates.REFILL_MILK:
            self.coffee_machine.milk = 10
            barkeeper.item = None
            return True
        return False


class CoffeeMachine(AbstractSprite):
    def __init__(self):
        super().__init__()
        self.tile_rect = Rect(9, 3, 1, 2)
        self.renderable = False
        self.state = MachineStates.NOT_USED
        self.obstacle = True
        
        self.coffee_grounds = 0
        self.milk: int = 10
        self.coffee: int = 50
        self.last_coffee: OrderWalkers = None
        self.coffee_time = time.time()

        self.closeup = CoffeeMachineCloseup(self)

        self.bubble = None

    def update(self, context: Context):
        if not self.bubble:
            self.bubble = SpeechBubble(self)
            self.bubble.content = MachineStatesContent(self.state)
            context.current_room.bubbles.append(self.bubble)

        if self.state is MachineStates.BLOCKED:
            if time.time() - self.coffee_time > 5:
                self.state = MachineStates.COFFEE_READY

        if self.state is not MachineStates.BLOCKED:
            for event in context.events:
                if (
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN)
                    and (self.state is not MachineStates.COFFEE_READY)
                ):
                    for sprite in context.current_room.sprites:
                        if type(sprite) == BarKeeper:
                            if sprite.looks_at(self):
                                self.state = MachineStates.IN_USE
                                context.closeup = self.closeup
                if (
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN)
                    and (self.state is MachineStates.COFFEE_READY)
                ):
                    for sprite in context.current_room.sprites:
                        if type(sprite) == BarKeeper:
                            if sprite.looks_at(self):
                                sprite.item = self.last_coffee
                                self.state = MachineStates.NOT_USED
