from pygame.event import Event

from .room import Room

class Context(object):
    def __init__(self):
        self.events: List[Event] = []
        self.room: Room = None
        self.delta_t = 0
