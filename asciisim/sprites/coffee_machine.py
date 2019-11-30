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
        if (
                (time.time() - self.coffee_time >= 20) and
                (self.state is not MachineStates.NOT_USED) and
                (self.state is not MachineStates.IN_USE)
        ):
            self.state = MachineStates.COFFEE_READY

        for event in context.events:
            if (
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_q)
                    and (self.state is not MachineStates.BLOCKED)
                    and (self.state is not MachineStates.COFFEE_READY)
            ):
                for sprite in context.current_room.sprites:
                    if type(sprite) == BarKeeper:
                        if sprite.is_near(self):
                            self.state = MachineStates.IN_USE
            if (
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN)
                    and (self.state is MachineStates.COFFEE_READY)
            ):
                for sprite in context.current_room.sprites:
                    if type(sprite) == BarKeeper:
                        if sprite.is_near(self):
                            # TODO: return coffee to barkeeper
                            pass

        # get broken status
        if self.coffee_grounds >= 15 and (not self.status_displayed):
            try:
                self.broken_status.remove(MachineStates.ALL_GOOD)
            except ValueError:
                pass
            except:
                raise Exception("Could not remove state")
            self.broken_status.append(MachineStates.CLEAR_COFFEE)
        elif self.sewage >= 15 and (not self.status_displayed):
            try:
                self.broken_status.remove(MachineStates.ALL_GOOD)
            except ValueError:
                pass
            except:
                raise Exception("Could not remove state")
            self.broken_status.append(MachineStates.CLEAR_WATER)
        elif self.milk <= 0 and (not self.status_displayed):
            try:
                self.broken_status.remove(MachineStates.ALL_GOOD)
            except ValueError:
                pass
            except:
                raise Exception("Could not remove state")
            self.broken_status.append(MachineStates.REFILL_MILK)
        elif self.coffee <= 0 and (not self.status_displayed):
            try:
                self.broken_status.remove(MachineStates.ALL_GOOD)
            except ValueError:
                pass
            except:
                raise Exception("Could not remove state")
            self.broken_status.append(MachineStates.REFILL_COFFEE)

        if self.state is MachineStates.IN_USE:
            # What to do generally:
            # - open interface
            context.closeup = self.closeup
            # check if something is missing/broken
            if self.broken_status[0] is not MachineStates.ALL_GOOD:
                # What to do when broken:
                # - check what is broken
                # - display what is broken
                # - start repair routine
                # - unlock machine
                for machine_state in self.broken_status:
                    if machine_state is MachineStates.CLEAR_COFFEE:
                        for event in context.events:
                            # TODO: hardcoded button: change to mouse input
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                                self.coffee_grounds = 0
                                self.broken_status.remove(MachineStates.CLEAR_COFFEE)
                    elif machine_state is MachineStates.CLEAR_WATER:
                        for event in context.events:
                            # TODO: hardcoded button: change to mouse input
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                                self.sewage = 0
                                self.broken_status.remove(MachineStates.CLEAR_WATER)
                    elif machine_state is MachineStates.REFILL_MILK:
                        for event in context.events:
                            # TODO: hardcoded button: change to mouse input
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                                self.milk = 10
                                self.broken_status.remove(MachineStates.REFILL_MILK)
                    elif machine_state is MachineStates.REFILL_COFFEE:
                        for event in context.events:
                            # TODO: hardcoded button: change to mouse input
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                                self.coffee = 50
                                self.broken_status.remove(MachineStates.REFILL_COFFEE)

            # What to do when not broken:
            # - check button status (e.g. make coffee, ...)
            # - block interface
            # - close interface
            # - display status
            # - make coffee
            # TODO: Get status of "Buttons" (e.g. make coffee, ...)

        for machine_state in self.broken_status:
            if (
                    (machine_state is MachineStates.CLEAR_COFFEE)
                    and (not self.status_displayed)
            ):
                self.status_displayed = True
            elif (
                    (machine_state is MachineStates.CLEAR_WATER)
                    and (not self.status_displayed)
            ):
                self.status_displayed = True
            elif (
                    (machine_state is MachineStates.REFILL_MILK)
                    and (not self.status_displayed)
            ):
                self.status_displayed = True
            elif (
                    (machine_state is MachineStates.REFILL_COFFEE)
                    and (not self.status_displayed)
            ):
                context.rooms["bar"].sprites.append(
                    StaticSprite(
                        Rect(9, 1, 1, 1),
                        pygame.image.load(IMG_DIR + "coffee_machine/no_coffee.png")
                    )
                )
                self.status_displayed = True
            elif machine_state is MachineStates.NOT_USED:
                pass

    def use_sprite(self):
        # TODO: Check for Pot
        self.state = MachineStates.IN_USE

    @property
    def pot_status(self):
        return self.pot

    def set_pot(self, new_status):
        self.pot = new_status

    def make_coffee(self, coffee_type: CoffeeTypes):

        if self.status_displayed:
            # TODO: If there is any broken status: coffee can not be made
            return

        self.coffee -= 1
        self.coffee_grounds += 1
        self.sewage += 0.2

        if coffee_type is CoffeeTypes.MAKE_COFFEE_MILK:
            self.milk -= 1
            self.sewage += 0.1

        self.last_coffee = coffee_type
        self.coffee_time = time.time()
