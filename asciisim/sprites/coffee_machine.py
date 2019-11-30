import pygame

from .bar_keeper import BarKeeper

from .sprite_enums import States
from .sprite_enums import CoffeeStates
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
            SpritePosition(9, 2),
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

    def update(self, context: Context):
        # TODO: Get state of the coffee machine (is it in use or broken)
        for event in context.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                for sprite in context.current_room.sprites:
                    if type(sprite) == BarKeeper:
                        if sprite.position.is_near(self.position):
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

        for machine_state in self.broken_status:
            # TODO: For each state: Show extra image for status
            if machine_state is CoffeeStates.CLEAR_COFFEE and not self.status_displayed:
                self.status_displayed = True
            elif machine_state is CoffeeStates.CLEAR_WATER and not self.status_displayed:
                self.status_displayed = True
            elif machine_state is CoffeeStates.REFILL_MILK and not self.status_displayed:
                self.status_displayed = True
            elif machine_state is CoffeeStates.REFILL_COFFEE and not self.status_displayed:
                context.room.sprites.append(
                    StaticSprite(
                        SpritePosition(10, 1),
                        pygame.image.load(IMG_DIR + "coffee_machine/no_coffee.png")
                    )
                )
                self.status_displayed = True
            elif machine_state is CoffeeStates.ALL_GOOD:
                pass
            else:
                raise Exception("Status {} not supported".format(str(self.broken_status)))

    def use_sprite(self):
        # TODO: Check for Pot
        self.state = States.IN_USE

    @property
    def pot_status(self):
        return self.pot

    def set_pot(self, new_status):
        self.pot = new_status
        
