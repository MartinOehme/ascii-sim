from pygame import Rect


class SpritePosition(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @property
    def rect(self):
        return Rect(
            135 * self.x + 435 + 68,
            135 * self.y + 68,
            135,
            135
        )
