import pygame
from pygame import Rect
from pygame import Surface

from ..base.game_object import GameObject


class Menu(GameObject):
    WIDTH = 1920
    HEIGHT = 1080

    def __init__(self):
        self.controls = []
        self.control_index = 0
        self.renderable = False
        self.tile_rect = Rect(0, 0, 0, 0)

    def add_control(self, control):
        if not self.controls:
            control.selected = True
        self.controls.append(control)

    def select_control(self, index):
        self.active_control.selected = False
        self.control_index = index
        self.active_control.selected = True

    @property
    def control_sprites(self):
        return self.controls

    def next_control(self):
        if len(self.controls) < 2:
            return

        if self.control_index < len(self.controls) - 1:
            self.select_control(self.control_index + 1)
        else:
            self.select_control(0)

    def previous_control(self):
        if len(self.controls) < 2:
            return

        if self.control_index == 0:
            self.select_control(len(self.controls) - 1)
        else:
            self.select_control(self.control_index - 1)

    def update(self, context):
        for event in context.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                    self.previous_control()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                    self.next_control()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for index, control in enumerate(self.controls):
                    if control.rect.collidepoint(*pos):
                        self.select_control(index)

    @property
    def active_control(self):
        return self.controls[self.control_index]
