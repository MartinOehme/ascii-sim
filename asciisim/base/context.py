from typing import Dict, List

from pygame.event import Event

from .room import Room
from.closeup import Closeup


class Context(object):
    BAR_ROOM = "bar"
    STORE_ROOM = "store"

    def __init__(self):
        self.events: List[Event] = []
        self.room: Room = None
        self.rooms: Dict[str, Room] = {}
        self.room_key: str = ""
        self.closeup: Closeup = None
        self.delta_t = 0
        self.change_room = False

    def set_room(self, key) -> None:
        if key in self.rooms:
            self.room_key = key
            self.change_room = True

    @property
    def current_room(self) -> Room:
        return self.rooms[self.room_key]
