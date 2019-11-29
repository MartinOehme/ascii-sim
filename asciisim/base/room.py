from pygame import Surface


class Room(object):
    def __init__(self):
        self.background: Surface = None
        self.sprites = []
