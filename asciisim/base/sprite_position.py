from pygame import Rect

class SpritePosition(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @property
    def rect(self):
        return Rect(72 * self.x, 72 * self.y, 72, 72)
