#!/usr/bin/env python
"""This script contains solvers and heuristics for solving a maze."""

import pygame
from math import sqrt
from Queue import PriorityQueue

LAWN = (124, 252, 0)
GREEN = (0, 255, 0)
LIME = (50, 205, 50)


def manhattan(x1, y1, x2, y2):
    """Manhattan distance formula"""
    return abs(x2 - x1) + abs(y2 - y1)


def chebyshev(x1, y1, x2, y2):
    """Chebyshev distance formula"""
    return max(abs(x2 - x1), abs(y2 - y1))


def euclidean(x1, y1, x2, y2):
    """Euclidean distance formula"""
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)


def a_star(screen, maze, heuristic):
    """Solve maze using A* search algorithm
    Priority Queue, priority = heuristic function (Manhattan, Chebyshev, Euclidean)
    Retrieve a cell with lowest priority from the pq, add unvisited
    neighbors to pq."""

    q = PriorityQueue()
    visited = set()
    sx, sy, fx, fy = 0, 0, 0, 0
    height = len(maze)
    width = len(maze[0])

    for x in xrange(height):
        for y in xrange(width):
            if maze[x][y] == 'S':
                sx, sy = x, y
            if maze[x][y] == 'F':
                fx, fy = x, y

    q.put((heuristic(sx, sy, fx, fy), sx, sy))

    while True:

        _, x, y = q.get()

        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for xn, yn in neighbors:
            if 0 <= xn < height and 0 <= yn < width:
                if maze[xn][yn] not in '-|' and (xn, yn) not in visited:
                    if maze[xn][yn] == 'F':
                        return
                    if maze[xn][yn] != 'S':
                        screen.fill(
                            GREEN, pygame.Rect(xn * 10, yn * 10, 10, 10))
                        pygame.display.update(
                            pygame.Rect(xn * 10, yn * 10, 10, 10))
                        visited.add((xn, yn))
                        q.put((heuristic(xn, yn, fx, fy), xn, yn))


def bidirectional_a_star(screen, maze, heuristic):
    """Solve maze using bidirectional A* search algorithm."""

    q, p = PriorityQueue(), PriorityQueue()
    visited1, visited2 = set(), set()
    sx, sy, fx, fy = 0, 0, 0, 0
    height = len(maze)
    width = len(maze[0])

    for x in xrange(height):
        for y in xrange(width):
            if maze[x][y] == 'S':
                sx, sy = x, y
            if maze[x][y] == 'F':
                fx, fy = x, y

    q.put((heuristic(sx, sy, fx, fy), sx, sy))
    p.put((heuristic(sx, sy, fx, fy), fx, fy))

    while True:
        _, x1, y1 = q.get()
        _, x2, y2 = p.get()

        neighbors1 = [(x1 - 1, y1), (x1 + 1, y1), (x1, y1 - 1), (x1, y1 + 1)]
        neighbors2 = [(x2 - 1, y2), (x2 + 1, y2), (x2, y2 - 1), (x2, y2 + 1)]

        for xn, yn in neighbors1:
            if 0 <= xn < height and 0 <= yn < width:
                if maze[xn][yn] not in '-|' and (xn, yn) not in visited1:
                    if maze[xn][yn] == 'F':
                        return
                    if maze[xn][yn] != 'S':
                        maze[xn][yn] = 'S'
                        screen.fill(
                            LAWN, pygame.Rect(xn * 10, yn * 10, 10, 10))
                        pygame.display.update(
                            pygame.Rect(xn * 10, yn * 10, 10, 10))
                        visited1.add((xn, yn))
                        q.put((heuristic(xn, yn, fx, fy), xn, yn))

        for xn, yn in neighbors2:
            if 0 <= xn < height and 0 <= yn < width:
                if maze[xn][yn] not in '-|' and (xn, yn) not in visited2:
                    if maze[xn][yn] == 'S':
                        return
                    if maze[xn][yn] != 'F':
                        maze[xn][yn] = 'F'
                        screen.fill(
                            LIME, pygame.Rect(xn * 10, yn * 10, 10, 10))
                        pygame.display.update(
                            pygame.Rect(xn * 10, yn * 10, 10, 10))
                        visited2.add((xn, yn))
                        p.put((heuristic(xn, yn, fx, fy), xn, yn))
