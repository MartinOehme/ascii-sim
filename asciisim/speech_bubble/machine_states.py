import pygame

from asciisim.res import IMG_DIR
from ..base.content import Content
from ..sprites.sprite_enums import MachineStates


class MachineStatesContent(Content):
    def __init__(self, state: MachineStates):
        super().__init__()
        self.state = state
        self.register_surface(
            f"image_{self.state.value}",
            lambda : pygame.image.load(IMG_DIR + "speech_bubbles/machine_states/" + state.value + ".png")
        )

    @property
    def image(self) -> pygame.Surface:
        return self.get_surface(f"image_{self.state.value}")