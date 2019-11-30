import pygame
from pygame import Rect
from pygame import Surface

from ..base.game_object import GameObject

class Menu(object):
    WIDTH = 1920
    HEIGHT = 1080
    
    def __init__(self):
        self.controls = []
        self.control_index = 0
        self.renderable = False
        
    def add_control(self, control):
        if not self.controls:
            control.renderable = True
        self.controls.append(control)
        
    @property
    def control_sprites(self):
        return self.controls
        
    def next_control(self):
        if len(self.controls) < 2:
            return

        self.active_control.renderable = False

        if self.control_index < len(self.controls) - 1:
            self.control_index += 1
        else:
            self.control_index = 0
            
        self.active_control.renderable = True

    def previous_control(self):
        if len(self.controls) < 2:
            return

        self.active_control.renderable = False
        
        if self.control_index == 0:
            self.control_index = len(self.controls) - 1
        else:
            self.control_index -= 1

        self.active_control.renderable = True

    def update(self, context):
        for event in context.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                    self.previous_control()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                    self.next_control()
        
    @property
    def active_control(self):
        return self.controls[self.control_index]
        
