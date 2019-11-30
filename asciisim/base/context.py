from typing import Dict, List

from pygame.event import Event

from .room import Room


class Context(object):
    BAR_ROOM = "bar"
    STORE_ROOM = "store"

    def __init__(self):
        self.events: List[Event] = []
        self.rooms: Dict[str, Room] = {}
        self.room_key: str = ""
        self.delta_t = 0

    def set_room(self, key) -> None:
        if key in self.rooms:
            self.room_key = key

    @property
    def current_room(self) -> Room:
        return self.rooms[self.room_key]
