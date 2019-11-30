from pygame import Rect


class SpritePosition(object):
    SIDEBAR_WIDTH = 435
    LEFT_BORDER = 68
    TOP_BORDER = 68
    TILE_SIZE = 135
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def is_near(self, position) -> bool:
        return (
                (self.x - position.x < 2 and not self.y - position.y) or
                (self.y - position.y < 2 and not self.x - position.x)
        )
    
    @property
    def rect(self):
        return Rect(
            self.TILE_SIZE * self.x + self.SIDEBAR_WIDTH + self.LEFT_BORDER,
            self.TILE_SIZE * self.y + self.TOP_BORDER,
            self.TILE_SIZE,
            self.TILE_SIZE
        )

    @classmethod
    def update_render_context(cls, render_context) -> None:
        cls.SIDEBAR_WIDTH = render_context.sidebar_width
        cls.LEFT_BORDER = render_context.left_border
        cls.TOP_BORDER = render_context.top_border
        cls.TILE_SIZE = render_context.tile_size

    
