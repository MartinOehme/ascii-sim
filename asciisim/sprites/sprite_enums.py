from enum import Enum


class States(Enum):
    NOT_USED = 0
    IN_USE = 1
    BROKEN = 2


class CoffeeStates(Enum):
    ALL_GOOD = 'all_good'
    CLEAR_COFFEE = 'clear_coffee'
    CLEAR_WATER = 'clear_water'
    REFILL_MILK = 'refill_milk'
    REFILL_COFFEE = 'refill_coffee'
    MAKE_COFFEE = 'make_coffee'
    MAKE_COFFEE_MILK = 'make_coffee_milk'


class CustomerStatus(Enum):
    WALKING = 0
    SITTING = 1


class OrderWalkers(Enum):
    COFFEE = 'coffee'
    COFFEE_MILK = 'coffee_milk'
    KOLLE_MATE = 'kolle_mate'
    PREMIUM_COLA = 'premium_cola'
    ZOTRINE = 'zotrine'
    RETURN_CUP = 'return_cup'
    GET_BROOM = 'get_broom'
    RETURN_BOTTLE = 'return_bottle'
    RETURN_BROOM = 'return_broom'


class OrderSitters(Enum):
    CHANGE_MUSIC = 'change_music'
    MUSIC_VOLUME_UP = 'music_volume_up'
    MUSIC_VOLUME_DOWN = 'music_volume_down'
    TEMPERATURE_UP = 'temperature_up'
    TEMPERATURE_DOWN = 'temperature_down'
