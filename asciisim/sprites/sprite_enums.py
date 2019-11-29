from enum import Enum


class States(Enum):
    NOT_USED = 0
    IN_USE = 1
    BROKEN = 2

class CoffeeStates(Enum):
    CLEAR_COFFEE = 0
    CLEAR_WATER = 1
    REFILL_MILK = 2
    REFILL_WATER = 3
