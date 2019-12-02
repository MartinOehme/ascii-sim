#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Tuple

import pygame
from pygame import Surface

from .base.game_object import GameObject
from .menu.control import Control


class RenderContext(object):
    def __init__(self, resolution: Tuple[int, int]):
        pygame.display.set_caption("AsciiSim")

        self.left_border: int = 0
        self.resolution: Tuple[int, int] = resolution
        self.scaling: float = 1
        self.screen: Surface = None
        self._sidebar_left = True
        self.sidebar_width: int = 0
        self.tile_size: int = 0
        self.top_border: int = 0

        self.resize(resolution)

    def resize(self, size: Tuple[int, int]):
        # Always force an aspect ration of 16 to 9
        width_size = (size[0], int(size[0] * 9 / 16))
        height_size = (int(size[1] * 16 / 9), size[1])

        if width_size[0] > height_size[0]:
            self.resolution = height_size
        else:
            self.resolution = width_size

        self.screen = pygame.display.set_mode(
            self.resolution,
            pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF
        )

        self.left_border = 68 * self.resolution[0] / 1920
        self.scaling = self.resolution[0] / 1920
        self.sidebar_width = 435 * self.resolution[0] / 1920
        self.tile_size = 135 * self.resolution[0] / 1920
        self.top_border = 68 * self.resolution[0] / 1920

        Control.update_render_context(self)
        GameObject.update_render_context(self)

    @property
    def sidebar_left(self):
        return self._sidebar_left

    @sidebar_left.setter
    def sidebar_left(self, value):
        if value == self._sidebar_left:
            return

        self._sidebar_left = value

        Control.update_render_context(self)
        GameObject.update_render_context(self)
