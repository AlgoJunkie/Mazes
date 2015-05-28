#!/usr/bin/env python
"""This script contains maze generating algorithms."""

from random import shuffle, random
import pygame
from pygame.locals import *

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


def binary_tree(screen, maze):
    """Generate maze using binary tree algorithm:
    Treat the top-left of the maze as the root of the binary tree
    For every cell in the maze, open a wall to the left and to the right"""

    height = len(maze)
    width = len(maze[0])

    for x in xrange(1, height, 2):
        for y in xrange(1, width, 2):
            if x - 1 == y - 1 == 0:
                pass
            elif x - 1 == 0 or y - 1 == 0:
                a, b = [(x - 1, y), (x, y - 1)][x - 1 == 0]
                maze[a][b] = ' '
                screen.fill(WHITE, pygame.Rect(a * 10, b * 10, 10, 10))
                pygame.display.update(pygame.Rect(a * 10, b * 10, 10, 10))
            else:
                a, b = [(x - 1, y), (x, y - 1)][random() > 0.5]
                maze[a][b] = ' '
                screen.fill(WHITE, pygame.Rect(a * 10, b * 10, 10, 10))
                pygame.display.update(pygame.Rect(a * 10, b * 10, 10, 10))


def depth_first_search(screen, maze):
    """Generate maze using depth first search algorithm
    While all cells have not been visited,
    randomly open a neighboring wall of an unvisited neighbor
    if no neighbor is unvisited, backtrack"""

    height = len(maze)
    width = len(maze[0])

    stack = [(1, 1)]
    unvisited = set()

    for i in xrange(1, height, 2):
        for j in xrange(1, width, 2):
            if (i, j) != stack[-1]:
                unvisited.add((i, j))

    while unvisited:
        x, y = stack[-1]

        neighbors = [
            (x - 2, y, x - 1, y),
            (x + 2, y, x + 1, y),
            (x, y - 2, x, y - 1),
            (x, y + 2, x, y + 1)
        ]
        shuffle(neighbors)
        backtrack = True

        for xn, yn, xw, yw in neighbors:
            if 0 <= xn < height and 0 <= yn < width and (xn, yn) in unvisited:
                backtrack = False
                maze[xw][yw] = ' '

                # Set removed walls to white
                screen.fill(WHITE, pygame.Rect(xw * 10, yw * 10, 10, 10))
                pygame.display.update(pygame.Rect(xw * 10, yw * 10, 10, 10))

                stack.append((xn, yn))
                unvisited.remove((xn, yn))
                break

        if backtrack:
            stack.pop()


def random_kruskal(screen, maze):
    """Create a list of walls that divide cells, and a set of every cell
    For every wall (in random order)
    If cells divided by wall are not in the same set, remove wall, join sets
    """

    class UnionFind:

        """Use UnionFind data structure for union and find operations of cells
        Use tuple to keep track of set for each cell
        Use size to add smaller trees into larger trees (flattening)"""

        def __init__(self, height, width):
            self.id = [[0] * (width) for _ in xrange(height)]
            self.size = [[1] * (width) for _ in xrange(height)]
            for x in xrange(height):
                for y in xrange(width):
                    self.id[x][y] = (x, y)

        def root(self, x, y):
            """Find root of a given cell"""
            while (x, y) != self.id[x][y]:
                a, b = self.id[x][y]
                self.id[x][y] = self.id[a][b]
                x, y = self.id[x][y]
            return x, y

        def union(self, x1, y1, x2, y2):
            """Join cells, adding smaller tree into the larger (flattening tree)"""
            i1, j1 = self.id[x1][y1]
            i2, j2 = self.id[x2][y2]
            if self.size[i1][j1] < self.size[i2][j2]:
                self.id[i1][j1] = (i2, j2)
                self.size[i2][j2] += self.size[i1][j1]
            else:
                self.id[i2][j2] = (i1, j1)
                self.size[i1][j1] += self.size[i2][j2]

    height = len(maze)
    width = len(maze[0])
    walls = []
    cells = []

    # Grab all walls that divide cells, and all cells
    for i in xrange(1, height - 1, 2):
        for j in xrange(2, width - 1, 2):
            walls.append((i, j))

    for i in xrange(2, height - 1, 2):
        for j in xrange(1, width - 1, 2):
            walls.append((i, j))

    for i in xrange(height):
        for j in xrange(width):
            cells.append(set((i, j)))

    uf = UnionFind(height, width)
    shuffle(walls)

    for x, y in walls:
        # If wall divides two cells that are in different sets, eliminate wall
        if maze[x][y] == '|':
            if not uf.root(x, y - 1) == uf.root(x, y + 1):
                uf.union(x, y - 1, x, y + 1)
                maze[x][y] = ' '
                screen.fill(WHITE, pygame.Rect(x * 10, y * 10, 10, 10))
                pygame.display.update(pygame.Rect(x * 10, y * 10, 10, 10))
        if maze[x][y] == '-':
            if not uf.root(x - 1, y) == uf.root(x + 1, y):
                uf.union(x - 1, y, x + 1, y)
                maze[x][y] = ' '
                screen.fill(WHITE, pygame.Rect(x * 10, y * 10, 10, 10))
                pygame.display.update(pygame.Rect(x * 10, y * 10, 10, 10))
    return maze
