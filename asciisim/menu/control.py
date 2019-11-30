from pygame import Rect

class Control(object):
    SCALING = 1
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height

    @property
    def rect(self) -> Rect:
        return Rect(
            self.x * self.SCALING,
            self.y * self.SCALING,
            self.width * self.SCALING,
            self.height * self.SCALING
        )

    @classmethod
    def update_render_context(cls, render_context) -> None:
        cls.SCALING = render_context.scaling

