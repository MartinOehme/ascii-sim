from enum import Enum


class States(Enum):
    NOT_USED = 0
    IN_USE = 1
    BROKEN = 2


class CoffeeStates(Enum):
    ALL_GOOD = 0
    CLEAR_COFFEE = 1
    CLEAR_WATER = 2
    REFILL_MILK = 3
    REFILL_COFFEE = 4
    MAKE_COFFEE = 5
    MAKE_COFFEE_MILK = 6
