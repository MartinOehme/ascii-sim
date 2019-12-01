from typing import Dict, List

from pygame.event import Event

from.closeup import Closeup


class Context(object):
    BAR_ROOM = "bar"
    STORE_ROOM = "store"

    def __init__(self):
        self.events: List[Event] = []
        self.room = None
        self.rooms = {}
        self.room_key: str = ""
        self.closeup: Closeup = None
        self.delta_t = 0
        self.change_room = False

    def set_room(self, key) -> None:
        if key in self.rooms:
            self.room_key = key
            self.change_room = True

    @property
    def current_room(self):
        return self.rooms[self.room_key]
