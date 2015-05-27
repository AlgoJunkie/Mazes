import pygame, sys, time
from pygame.locals import *
from Queue import PriorityQueue

green = (0,255,0)

def solve_maze_a_star(screen,maze):
    # Solve maze using A* search algorithm
    # Initialize Priority Queue with priority = Manhattan distance

    def manhattan(x1,y1,x2,y2):
        return abs(x2-x1) + abs(y2-y1)

    q = PriorityQueue()
    visited = set()
    sx,sy,fx,fy = 0,0,0,0
    height = len(maze); width = len(maze[0])

    for x in xrange(height):
        for y in xrange(width):
            if maze[x][y] == 'S':
                sx,sy = x,y
            if maze[x][y] == 'F':
                fx,fy = x,y

    q.put((manhattan(sx,sy,fx,fy),sx,sy))

    while True:

        p,x,y = q.get()

        if maze[x][y] == 'F':
            break

        neighbors = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
        for xn,yn in neighbors:
            if 0 <= xn < height and 0 <= yn < width:
                if maze[xn][yn] not in '-|' and (xn,yn) not in visited:
                    screen.fill(green,pygame.Rect(xn*10,yn*10,10,10))
                    pygame.display.update(pygame.Rect(xn*10,yn*10,10,10))
                    visited.add((xn,yn))
                    q.put((manhattan(xn,yn,fx,fy),xn,yn))
