#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame

from .game import Game

class AsciiSim(object):
    def __init__(self):
        self.game = None
        self.running = True
        self.screen = None
        
    def initialize(self):
        if not pygame.font:
            print('Error, pygame.font not found!')
            sys.exit(1)
        if not pygame.mixer:
            print('Error, pygame.mixer not found!')
            sys.exit(1)
        # Pre initialize the mixer with a smaller buffer size, this solves
        # problems.
        pygame.mixer.pre_init(22050, -16, 2, 512)
        pygame.joystick.init()
        pygame.init()

        self.screen = pygame.display.set_mode((1920, 1080))
        self.game = Game(self.screen)

    def main(self):
        self.initialize()
        self.game.main()
    
