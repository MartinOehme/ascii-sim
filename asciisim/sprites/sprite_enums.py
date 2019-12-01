from enum import Enum

from ..res import SOUND_DIR

class MachineStates(Enum):
    ALL_GOOD = 'all_good'
    # Closeup not open
    NOT_USED = 'not_used'
    # Closeup open
    IN_USE = 'in_use'
    # Cannot open closeup
    BLOCKED = 'blocked'
    # Coffee is ready
    COFFEE_READY = 'coffee_ready'
    # Empty the coffee dregs
    CLEAR_COFFEE = 'clear_coffee'
    # Bring water out
    CLEAR_WATER = 'clear_water'
    REFILL_MILK = 'refill_milk'
    REFILL_COFFEE = 'refill_coffee'


class CoffeeTypes(Enum):
    NORMAL_COFFEE = 0
    COFFEE_MILK = 1


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


class CustomerHappiness(Enum):
    NEUTRAL = 'neutral'
    HAPPY = 'happy'
    UNHAPPY = 'unhappy'


class MusicTracks(Enum):
    MUSIC_OFF = None
    # https://freesound.org/s/399821/
    TRACK1 = SOUND_DIR + "track1.mp3"
    # https://freesound.org/s/415511/
    TRACK2 = SOUND_DIR + "track2.mp3"


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
