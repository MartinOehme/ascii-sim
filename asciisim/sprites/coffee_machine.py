import pygame
import time

from .sprite_enums import States, CoffeeStates, CoffeeTypes
from .static_sprite import StaticSprite

from ..base.sprite_position import SpritePosition
from ..base.context import Context
from ..base.closeup import Closeup
from ..res import IMG_DIR


class CoffeeMachine(StaticSprite):
    def __init__(self):
        super().__init__(
            SpritePosition(9, 3),
            pygame.image.load(IMG_DIR + "coffee_machine/coffee_machine.png")
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

        self.last_coffee: CoffeeTypes = None

        self.coffee_time = time.time()

        self.closeup = Closeup(
            IMG_DIR + "coffee_machine/coffee_machine_closeup.png"
        )

        self.closeup.sprites.append(
            StaticSprite(
                SpritePosition(5, 5),
                IMG_DIR + "coffee_machine/coffee.png"
            )
        )

    def update(self, context: Context):

        if (time.time() - self.coffee_time >= 20) and (self.state is not States.NOT_USED) and (self.state is not States.IN_USE):
            self.state = States.READY

        # TODO: Get state of the coffee machine (is it in use or broken)
        if keyboard.is_pressed('q') and (self.state is not States.BLOCKED) and (self.state is not States.READY):
            self.state = States.IN_USE
        for event in context.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.state = States.IN_USE

        # get broken status
        if self.coffee_grounds >= 15:
            try:
                self.broken_status.remove(CoffeeStates.ALL_GOOD)
            except ValueError:
                pass
            except:
                raise Exception("Could not remove state")
            self.broken_status.append(CoffeeStates.CLEAR_COFFEE)
        elif self.sewage >= 15:
            try:
                self.broken_status.remove(CoffeeStates.ALL_GOOD)
            except ValueError:
                pass
            except:
                raise Exception("Could not remove state")
            self.broken_status.append(CoffeeStates.CLEAR_WATER)
        elif self.milk <= 0:
            try:
                self.broken_status.remove(CoffeeStates.ALL_GOOD)
            except ValueError:
                pass
            except:
                raise Exception("Could not remove state")
            self.broken_status.append(CoffeeStates.REFILL_MILK)
        elif self.coffee <= 0:
            try:
                self.broken_status.remove(CoffeeStates.ALL_GOOD)
            except ValueError:
                pass
            except:
                raise Exception("Could not remove state")
            self.broken_status.append(CoffeeStates.REFILL_COFFEE)

        if self.state is States.IN_USE:
            context.closeup = self.closeup
            # TODO: Get status of "Buttons" (e.g. make coffee, ...)
            if keyboard.is_pressed('n'):
                self.state = States.BLOCKED
                context.closeup = None
                self.make_coffee(CoffeeTypes.MAKE_COFFEE)
            if keyboard.is_pressed('m'):
                self.state = States.BLOCKED
                context.closeup = None
                self.make_coffee(CoffeeTypes.MAKE_COFFEE_MILK)

        for machine_state in self.broken_status:
            if (machine_state is CoffeeStates.CLEAR_COFFEE) and (not self.status_displayed):
                self.status_displayed = True
            elif (machine_state is CoffeeStates.CLEAR_WATER) and (not self.status_displayed):
                self.status_displayed = True
            elif (machine_state is CoffeeStates.REFILL_MILK) and (not self.status_displayed):
                self.status_displayed = True
            elif (machine_state is CoffeeStates.REFILL_COFFEE) and (not self.status_displayed):
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
        self.coffee -= 1
        self.coffee_grounds += 1
        self.sewage += 0.2

        if coffee_type is CoffeeTypes.MAKE_COFFEE_MILK:
            self.milk -= 1
            self.sewage += 0.1

        self.last_coffee = coffee_type
        self.coffee_time = time.time()
