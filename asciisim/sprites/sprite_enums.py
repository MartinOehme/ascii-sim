from enum import Enum


class States(Enum):
    NOT_USED = 0
    IN_USE = 1
    BROKEN = 2
    BLOCKED = 3
    READY = 4


class CoffeeStates(Enum):
    ALL_GOOD = 0
    CLEAR_COFFEE = 1
    CLEAR_WATER = 2
    REFILL_MILK = 3
    REFILL_COFFEE = 4


class CoffeeTypes(Enum):
    MAKE_COFFEE = 0
    MAKE_COFFEE_MILK = 1


class CustomerStatus(Enum):
    WALKING = 0
    SITTING = 1


class OrderWalkers(Enum):
    COFFEE = 0
    COFFEE_MILK = 1
    KOLLE_MATE = 2
    PREMIUM_COLA = 3
    ZOTRINE = 4
    RETURN_CUP = 5
    GET_BROOM = 6
    RETURN_BOTTLE = 7
    RETURN_BROOM = 8


class OrderSitters(Enum):
    CHANGE_MUSIC = 0
    MUSIC_VOLUME_UP = 1
    MUSIC_VOLUME_DOWN = 2
    TEMPERATURE_UP = 3
    TEMPERATURE_DOWN = 4
