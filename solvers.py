#!/usr/bin/env python
"""This script contains solvers and heuristics for solving a maze."""

from math import sqrt
from Queue import PriorityQueue
from settings import START, FINISH, GREEN, paint


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

    # Grab coordinates of start and endpoints of the path
    for x in xrange(height):
        for y in xrange(width):
            if maze[x][y] == 'S':
                sx, sy = x, y
            if maze[x][y] == 'F':
                fx, fy = x, y

    q.put((heuristic(sx, sy, fx, fy), sx, sy))

    # On each iteration, retrieve object with the lowest value
    # While endpoint hasn't been reached, add all visitable neighbors to pq
    while True:

        _, x, y = q.get()
        visited.add((x, y))

        if maze[x][y] not in 'SF':
            paint(screen, x, y, GREEN)
        if maze[x][y] == 'F':
            return

        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for xn, yn in neighbors:
            if 0 <= xn < height and 0 <= yn < width:
                if maze[xn][yn] not in '-|' and (xn, yn) not in visited:
                    q.put((heuristic(xn, yn, fx, fy), xn, yn))


def bidirectional_a_star(screen, maze, heuristic):
    """Solve maze using bidirectional A* search algorithm."""

    height = len(maze)
    width = len(maze[0])
    pq = [PriorityQueue(), PriorityQueue()]
    visited = [set(), set()]
    sx, sy, fx, fy = 0, 0, 0, 0

    # Grab start and end coordinates of path
    for x in xrange(height):
        for y in xrange(width):
            if maze[x][y] == 'S':
                sx, sy = x, y
            if maze[x][y] == 'F':
                fx, fy = x, y

    priority = heuristic(sx, sy, fx, fy)

    pq[0].put((priority, sx, sy))
    pq[1].put((priority, fx, fy))

    # Same as a*, but begin path from both directions
    # Terminate when paths intersect
    while True:
        _, x1, y1 = pq[0].get()
        _, x2, y2 = pq[1].get()

        visited[0].add((x1, y1))
        visited[1].add((x2, y2))

        if (x1, y1) in visited[1] or (x2, y2) in visited[0]:
            if (x1, y1) == (x2, y2):
                paint(screen, x1, y1, START)
            return

        if maze[x1][y1] and maze[x2][y2] not in 'SF':
            paint(screen, x1, y1, START)
            paint(screen, x2, y2, FINISH)

        neighbors = [[(x1 - 1, y1), (x1 + 1, y1), (x1, y1 - 1), (x1, y1 + 1)],
                     [(x2 - 1, y2), (x2 + 1, y2), (x2, y2 - 1), (x2, y2 + 1)]]

        for xn, yn in neighbors[0]:
            if 0 <= xn < height and 0 <= yn < width \
                    and maze[xn][yn] not in '-|SF' \
                    and (xn, yn) not in visited[0]:
                pq[0].put((heuristic(xn, yn, fx, fy), xn, yn))

        for xn, yn in neighbors[1]:
            if 0 <= xn < height and 0 <= yn < width \
                    and maze[xn][yn] not in '-|SF' \
                    and (xn, yn) not in visited[1]:
                pq[1].put((heuristic(xn, yn, sx, sy), xn, yn))
