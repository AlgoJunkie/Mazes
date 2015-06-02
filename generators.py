#!/usr/bin/env python
"""This script contains maze generating algorithms."""

from random import shuffle, random, sample
from settings import WHITE, paint


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
                paint(screen, a, b, WHITE)
            else:
                a, b = [(x - 1, y), (x, y - 1)][random() > 0.5]
                maze[a][b] = ' '
                paint(screen, a, b, WHITE)


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
                paint(screen, xw, yw, WHITE)

                stack.append((xn, yn))
                unvisited.remove((xn, yn))
                break

        if backtrack:
            stack.pop()


def random_kruskal(screen, maze):
    """Create a list of walls that divide cells, and a set of every cell
    For every wall (in random order)
    If cells divided by wall are not in the same set, remove wall, join sets"""

    class UnionFind(object):

        """Use UnionFind data structure for union and find operations of cells
        Use tuple to keep track of set for each cell
        Use size to add smaller trees into larger trees (flattening)."""

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
                paint(screen, x, y, WHITE)
        if maze[x][y] == '-':
            if not uf.root(x - 1, y) == uf.root(x + 1, y):
                uf.union(x - 1, y, x + 1, y)
                maze[x][y] = ' '
                paint(screen, x, y, WHITE)
    return maze


def hunt_and_kill(screen, maze):
    '''Perform a random walk, open walls to neighbors.
    If all neighbors are visited, find first unvisited cell adjacent to a
    visited cell. Add this cell to the walk and repeat.'''

    height = len(maze)
    width = len(maze[0])

    visited = set((1, 1))
    cells = [maze[x][y] for y in xrange(height) for x in xrange(height)]
    filled = cells.count(' ')
    x, y = 1, 1

    neighbors = lambda x, y: [
        (x - 2, y, x - 1, y),
        (x + 2, y, x + 1, y),
        (x, y - 2, x, y - 1),
        (x, y + 2, x, y + 1)]

    def kill(screen, maze, visited):
        '''Find, open unvisited cell adjacent to visited cell.'''
        for h in xrange(1, height, 2):
            for w in xrange(1, width, 2):
                if (h, w) not in visited:
                    for xn, yn, xw, yw in neighbors(h, w):
                        if (xn, yn) in visited:
                            maze[xw][yw] = ' '
                            paint(screen, xw, yw, WHITE)
                            visited.add((h, w))
                            return h, w

    while len(visited) <= filled:

        hunt = True
        n = neighbors(x, y)
        shuffle(n)

        for xn, yn, xw, yw in n:
            if 0 <= xn < height and 0 <= yn < width:
                if (xn, yn) not in visited:
                    hunt = False
                    maze[xw][yw] = ' '
                    paint(screen, xw, yw, WHITE)
                    x, y = xn, yn
                    visited.add((xn, yn))
                    break

        if hunt:
            x, y = kill(screen, maze, visited)

    return maze


def random_prim(screen, maze):
    '''Choose a random wall that connects an unvisited cell to a visited cell.
    Terminate when all cells are connected to each other.'''

    height = len(maze)
    width = len(maze[0])
    frontier = set()  # <- Neighbors/walls of all nodes in the graph
    f = set()  # <- Dict with all x,y tuples in frontier
    graph = set((1, 1))  # <- All nodes in the graph

    neighbors = lambda x, y: [
        (x - 2, y, x - 1, y),
        (x + 2, y, x + 1, y),
        (x, y - 2, x, y - 1),
        (x, y + 2, x, y + 1)]

    for xn, yn, xw, yw in neighbors(1, 1):
        if 0 <= xn < height and 0 <= yn < width:
            frontier.add((xn, yn, xw, yw))
            f.add((xn, yn))

    while frontier:
        x, y, xw, yw = sample(frontier, 1)[0]
        frontier.remove((x, y, xw, yw))
        f.remove((x, y))
        maze[xw][yw] = ' '
        paint(screen, xw, yw, WHITE)
        graph.add((x, y))

        for x2, y2, xw2, yw2 in neighbors(x, y):
            if 0 <= x2 < height and 0 <= y2 < width:
                if (x2, y2) not in graph and (x2, y2) not in f:
                    frontier.add((x2, y2, xw2, yw2))
                    f.add((x2, y2))
    return maze
