import pygame
from pygame import Rect

from .context import Context
from .game_object import GameObject
from ..sprites.sprite_enums import OrderWalkers, MachineStates
from ..res import IMG_DIR
from ..res import FONT_DIR


class SideBar(GameObject):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(FONT_DIR + "Game_font.ttf", 50)
        self.is_left = True
        self.register_surface(
            "sidebar",
            lambda: pygame.image.load(IMG_DIR + "sidebar.png")
        )
        self.item = None
        self.score = 0
        for icon in OrderWalkers:
            self.register_surface(
                icon.value,
                lambda: pygame.transform.smoothscale(
                    pygame.image.load(
                        IMG_DIR +
                        f"speech_bubbles/order_walkers/{icon.value}.png"
                    ),
                    (300, 300)
                )
            )
        for icon in MachineStates:
            self.register_surface(
                icon.value,
                lambda: pygame.transform.smoothscale(
                    pygame.image.load(
                        IMG_DIR +
                        f"speech_bubbles/machine_states/{icon.value}.png"
                    ),
                    (300, 300)
                )
            )

    @property
    def image(self):
        surface = self.get_surface("sidebar").copy()
        scaling = self.TILE_SIZE / 135

        score = self.font.render(f"Score : {self.score}", 16, (255, 255, 255))
        score_size = score.get_size()
        score = pygame.transform.smoothscale(
            score,
            (
                int(score_size[0] * scaling),
                int(score_size[1] * scaling)
            )
        )
        surface.blit(
            score,
            (
                int(100 * scaling),
                int(1000 * scaling)
            )
        )

        if self.item:
            surface.blit(
                self.get_surface(self.item.value),
                Rect(
                    67.5 * scaling,
                    671.5 * scaling,
                    300 * scaling,
                    300 * scaling
                )
            )

        return surface

    def update(self, context):
        self.item = context.bar_keeper.item
        self.score = context.bar_keeper.earnings
        if context.room_key == Context.BAR_ROOM:
            self.is_left = True
        else:
            self.is_left = False

    @property
    def rect(self) -> Rect:
        img_size = self.image.get_size()
        left = 0
        scaling = self.TILE_SIZE / 135
        if not self.is_left:
            left = 1920 * scaling - img_size[0]
        return Rect(
            (left, 0),
            img_size
        )
