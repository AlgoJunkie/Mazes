from random import shuffle,random
import pygame, sys, time
from pygame.locals import *

black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)


def binary_tree(screen,maze):
    # Randomly color passages up or left

    height = len(maze); width = len(maze[0])

    for x in xrange(1,height,2):
        for y in xrange(1,width,2):
            if x-1 == y-1 == 0:
                pass
            elif x-1 == 0 or y-1 == 0:
                a,b = [(x-1,y),(x,y-1)][x-1 == 0]
                maze[a][b] = ' '
                screen.fill(white,pygame.Rect(a*10,b*10,10,10))
                pygame.display.update(pygame.Rect(a*10,b*10,10,10))
            else:
                a,b = [(x-1,y),(x,y-1)][random() > 0.5]
                maze[a][b] = ' '
                screen.fill(white,pygame.Rect(a*10,b*10,10,10))
                pygame.display.update(pygame.Rect(a*10,b*10,10,10))

def depth_first_search(screen,maze):
    height = len(maze); width = len(maze[0])

    stack = [(1,1)]
    unvisited = set()

    for i in xrange(1,height,2):
        for j in xrange(1,width,2):
            if (i,j) != stack[-1]:
                unvisited.add((i,j))

    while unvisited:
        x,y = stack[-1]

        neighbors = [
            (x-2,y,x-1,y),
            (x+2,y,x+1,y),
            (x,y-2,x,y-1),
            (x,y+2,x,y+1)
        ]
        shuffle(neighbors)
        backtrack = True

        for xn,yn,xw,yw in neighbors:
            if 0 <= xn < height and 0 <= yn < width and (xn,yn) in unvisited:
                backtrack = False
                maze[xw][yw] = ' '

                # Set removed walls to white
                screen.fill(white,pygame.Rect(xw*10,yw*10,10,10))
                pygame.display.update(pygame.Rect(xw*10,yw*10,10,10))

                stack.append((xn,yn))
                unvisited.remove((xn,yn))
                break

        if backtrack:
            stack.pop()
