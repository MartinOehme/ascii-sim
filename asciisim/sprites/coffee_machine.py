import pygame
import time

from .bar_keeper import BarKeeper

from .sprite_enums import States
from .sprite_enums import CoffeeStates
from .sprite_enums import CoffeeTypes
from .static_sprite import StaticSprite

from ..base.sprite_position import SpritePosition
from ..base.context import Context
from ..base.closeup import Closeup
from ..res import IMG_DIR

class CoffeeMachineCloseup(Closeup):
    def __init__(self, coffee_machine: 'CoffeeMachine'):
        super().__init__(IMG_DIR + "coffee_machine/coffee_machine_closeup.png")
        self.coffee_machine = coffee_machine
        self.sprites.append(
            StaticSprite(
                SpritePosition(5, 5),
                IMG_DIR + "coffee_machine/coffee.png"
            )
        )

    def update(self, context: Context) -> None:
        for event in context.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                context.closeup = None
                self.coffee_machine.state = States.NOT_USED
        
class CoffeeMachine(StaticSprite):
    def __init__(self):
        super().__init__(
            SpritePosition(9, 3),
            IMG_DIR + "coffee_machine/coffee_machine.png"
        )
        self.state = States.NOT_USED
        self.broken_status = list()
        self.broken_status.append(CoffeeStates.ALL_GOOD)
        self.status_displayed = False

        self.pot = False
        self.coffee_grounds = 0
        self.sewage = 0
        self.milk: int = 10
        self.coffee: int = 50

        self.closeup = CoffeeMachineCloseup(self)
        self.last_coffee: CoffeeTypes = None
        self.coffee_time = time.time()

    def update(self, context: Context):

        if (
                (time.time() - self.coffee_time >= 20) and
                (self.state is not States.NOT_USED) and
                (self.state is not States.IN_USE)
        ):
            self.state = States.READY

        for event in context.events:
            if (
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_q)
                    and (self.state is not States.BLOCKED)
                    and (self.state is not States.READY)
            ):
                for sprite in context.current_room.sprites:
                    if type(sprite) == BarKeeper:
                        if sprite.position.is_near(self.position):
                            self.state = States.IN_USE
            if (
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN)
                    and (self.state is States.READY)
            ):
                for sprite in context.current_room.sprites:
                    if type(sprite) == BarKeeper:
                        if sprite.position.is_near(self.position):
                            # TODO: return coffee to barkeeper
                            pass

        # get broken status
        if self.coffee_grounds >= 15 and (not self.status_displayed):
            try:
                self.broken_status.remove(CoffeeStates.ALL_GOOD)
            except ValueError:
                pass
            except:
                raise Exception("Could not remove state")
            self.broken_status.append(CoffeeStates.CLEAR_COFFEE)
        elif self.sewage >= 15 and (not self.status_displayed):
            try:
                self.broken_status.remove(CoffeeStates.ALL_GOOD)
            except ValueError:
                pass
            except:
                raise Exception("Could not remove state")
            self.broken_status.append(CoffeeStates.CLEAR_WATER)
        elif self.milk <= 0 and (not self.status_displayed):
            try:
                self.broken_status.remove(CoffeeStates.ALL_GOOD)
            except ValueError:
                pass
            except:
                raise Exception("Could not remove state")
            self.broken_status.append(CoffeeStates.REFILL_MILK)
        elif self.coffee <= 0 and (not self.status_displayed):
            try:
                self.broken_status.remove(CoffeeStates.ALL_GOOD)
            except ValueError:
                pass
            except:
                raise Exception("Could not remove state")
            self.broken_status.append(CoffeeStates.REFILL_COFFEE)

        if self.state is States.IN_USE:
            # What to do generally:
            # - open interface
            context.closeup = self.closeup
            # check if something is missing/broken
            if self.broken_status[0] is not CoffeeStates.ALL_GOOD:
                # What to do when broken:
                # - check what is broken
                # - display what is broken
                # - start repair routine
                # - unlock machine
                for machine_state in self.broken_status:
                    if machine_state is CoffeeStates.CLEAR_COFFEE:
                        for event in context.events:
                            # TODO: hardcoded button: change to mouse input
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                                self.coffee_grounds = 0
                                self.broken_status.remove(CoffeeStates.CLEAR_COFFEE)
                    elif machine_state is CoffeeStates.CLEAR_WATER:
                        for event in context.events:
                            # TODO: hardcoded button: change to mouse input
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                                self.sewage = 0
                                self.broken_status.remove(CoffeeStates.CLEAR_WATER)
                    elif machine_state is CoffeeStates.REFILL_MILK:
                        for event in context.events:
                            # TODO: hardcoded button: change to mouse input
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                                self.milk = 10
                                self.broken_status.remove(CoffeeStates.REFILL_MILK)
                    elif machine_state is CoffeeStates.REFILL_COFFEE:
                        for event in context.events:
                            # TODO: hardcoded button: change to mouse input
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                                self.coffee = 50
                                self.broken_status.remove(CoffeeStates.REFILL_COFFEE)

            # What to do when not broken:
            # - check button status (e.g. make coffee, ...)
            # - block interface
            # - close interface
            # - display status
            # - make coffee
            # TODO: Get status of "Buttons" (e.g. make coffee, ...)

        for machine_state in self.broken_status:
            if (
                    (machine_state is CoffeeStates.CLEAR_COFFEE)
                    and (not self.status_displayed)
            ):
                self.status_displayed = True
            elif (
                    (machine_state is CoffeeStates.CLEAR_WATER)
                    and (not self.status_displayed)
            ):
                self.status_displayed = True
            elif (
                    (machine_state is CoffeeStates.REFILL_MILK)
                    and (not self.status_displayed)
            ):
                self.status_displayed = True
            elif (
                    (machine_state is CoffeeStates.REFILL_COFFEE)
                    and (not self.status_displayed)
            ):
                context.rooms["bar"].sprites.append(
                    StaticSprite(
                        SpritePosition(9, 1),
                        pygame.image.load(IMG_DIR + "coffee_machine/no_coffee.png")
                    )
                )
                self.status_displayed = True
            elif machine_state is CoffeeStates.ALL_GOOD:
                pass

    def use_sprite(self):
        # TODO: Check for Pot
        self.state = States.IN_USE

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
