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


class OrderWalkers(Enum):
    HOT_DRINK = 0
    COLD_DRINK = 1
    RETURN_CUP = 2
    GET_BROOM = 3
    RETURN_BROOM = 4


class OrderSiters(Enum):
    CHANGE_MUSIC = 0
    MUSIC_VOLUME = 1
    CHANGE_TEMPERATURE = 3
