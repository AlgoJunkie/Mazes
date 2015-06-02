#!/usr/bin/env python
"""Constants, helper functions used by all maze files, such as cell dimension
and colors, painting function, etc."""

import pygame

START = (255, 255, 0)
GREEN = (0, 255, 0)
FINISH = (50, 205, 50)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
CELL = 10


def paint(screen, x, y, color):
    '''Given an x,y coordinate of the maze, paint a certain color'''
    screen.fill(color, pygame.Rect(y * CELL, x * CELL, CELL, CELL))
    pygame.display.update(pygame.Rect(y * CELL, x * CELL, CELL, CELL))
