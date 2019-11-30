from ..base.sprite_position import SpritePosition
from ..base.context import Context
from ..sprites.static_sprite import StaticSprite
from ..res import IMG_DIR


class Radiator(StaticSprite):
    def __init__(self, position: SpritePosition, temperature=22):
        super().__init__(
            position,
            IMG_DIR + "radiator.png"
        )

        self.temperature = temperature

    def update(self, context: Context):
        context.rooms["bar"].temperature = self.temperature

    def change_temperature(self, value):
        self.temperature += value


class MusicBox(StaticSprite):
    def __init__(self, position: SpritePosition, volume=50):
        super().__init__(
            position,
            IMG_DIR + "music_box.png"
        )

        self.volume = volume

    def update(self, context: Context):
        context.rooms["bar"].volume = self.volume

    def change_volume(self, value):
        self.volume += value
