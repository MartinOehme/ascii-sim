from typing import Dict, List

from pygame.event import Event

from .room import Room
from .closeup import Closeup

class Context(object):
    BAR_ROOM = "bar"
    STORE_ROOM = "store"

    def __init__(self):
        self.bar_keeper = None
        self.change_room = False
        self.closeup: Closeup = None
        self.delta_t = 0
        self.events: List[Event] = []
        self.keys_pressed = {}
        self.room: Room = None
        self.rooms: Dict[str, Room] = {}
        self.room_key: str = ""

    def set_room(self, key) -> None:
        if key in self.rooms:
            self.room_key = key
            self.change_room = True

    @property
    def current_room(self) -> Room:
        return self.rooms[self.room_key]
