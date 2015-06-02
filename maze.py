#!/usr/bin/env python
"""This script visualizes the maze constructed by a certain generator algorithm,
solver algorithm, and a heuristic."""

import pygame
import sys
from settings import CELL, BLACK, WHITE, BLUE
from generators import (binary_tree, depth_first_search, random_kruskal,
                        hunt_and_kill, random_prim)
from solvers import a_star, bidirectional_a_star, manhattan, chebyshev, euclidean


def generate_empty_maze(height, width):
    """Create corresponding ascii table used for keeping track of maze
    Ex: maze of height 3, width 3
    -------
    | | | |
    -------
    | | | |
    -------
    | | | |
    -------
    """
    maze = []
    for x in xrange(height * 2 + 1):
        if x % 2 == 0:
            maze.append(list('-' * (width * 2 + 1)))
        else:
            maze.append(list('| ' * width + '|'))
    return maze


def select_endpoint(x, y, marker, height, width, screen, maze):
    """Given x,y location, paint grid on pygame and set maze to marker"""
    if 0 <= x / CELL < height and 0 <= y / CELL < width:
        if maze[x / CELL][y / CELL] == ' ':
            pygame.draw.rect(
                screen, BLUE, pygame.Rect(y / CELL * CELL, x / CELL * CELL, CELL, CELL))
            pygame.display.update()
            maze[x / CELL][y / CELL] = marker
            return True


def visualize(height, width, generator_algorithm, solver_algorithm, heuristic):
    """Visualize construction and solution of mazes in Pygame, calling a
    maze generator algorithm, solver algorithm and heuristic."""

    maze = generate_empty_maze(height, width)
    height, width = len(maze), len(maze[0])
    start, end, solved = None, None, False

    # Initialize Pygame, Window Variables etc.
    pygame.init()
    pygame.display.set_caption('Maze Solver')
    window_height = max(200, height * CELL + 50)
    window_width = max(200, width * CELL + 50)
    screen = pygame.display.set_mode((window_width, window_height))

    # If cell is open, mark it as white, else mark walls as black
    for x in xrange(height):
        for y in xrange(width):
            if maze[x][y] != ' ':
                pygame.draw.rect(
                    screen, BLACK, pygame.Rect(y * CELL, x * CELL, CELL, CELL))
            else:
                pygame.draw.rect(
                    screen, WHITE, pygame.Rect(y * CELL, x * CELL, CELL, CELL))

    generator_algorithm(screen, maze)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # User input start and end points for a search algorithm
                y, x = event.pos
                if not start:
                    start = select_endpoint(
                        x, y, 'S', height, width, screen, maze)
                elif start and not end:
                    end = select_endpoint(
                        x, y, 'F', height, width, screen, maze)
        if start and end and not solved:
            solver_algorithm(screen, maze, heuristic)
            solved = True
