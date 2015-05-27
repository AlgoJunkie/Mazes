from random import shuffle,random
import pygame, sys, time
from pygame.locals import *
from generators import *
from solvers import *

def generate_empty_maze(height,width):
    height = [height+1,height][height % 2]
    maze = [list('| '*(width-1)+'|') if x%2 else list('-' * (width*2-1)) for x in xrange(height)]
    return maze

def visualize(height,width,generator_algorithm,solver_algorithm):
    # Visualize construction of binary tree maze in Pygame

    maze = generate_empty_maze(height,width)
    height, width = len(maze),len(maze[0])
    start, end = None, None

    # Initialize Pygame, Set Colors, Window Variables etc.
    pygame.init()
    pygame.display.set_caption('Maze Solver')

    window_height = max(200,width*10+50)
    window_width = max(200,height*10+50)
    screen = pygame.display.set_mode((window_width,window_height),0,32)

    
    # If cell is open, mark it as white, else mark it as black
    for x in xrange(height):
        for y in xrange(width):
            if maze[x][y] != ' ':
                pygame.draw.rect(screen,black,pygame.Rect(x*10,y*10,10,10))
            else:
                pygame.draw.rect(screen,white,pygame.Rect(x*10,y*10,10,10))

    generator_algorithm(screen,maze)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # User input start and end points for a search algorithm
                if not start:
                    x, y = event.pos
                    if 0 <= x/10 < height and 0 <= y/10 < width:
                        if maze[x/10][y/10] == ' ':
                            pygame.draw.rect(screen,green,pygame.Rect(x/10*10,y/10*10,10,10))
                            pygame.display.update()
                            start = (x/10 * 10, y/10 * 10)
                            maze[start[0]/10][start[1]/10] = 'S'
                elif start and not end:
                    x, y = event.pos
                    if 0 <= x/10 < height and 0 <= y/10 < width:
                        if maze[x/10][y/10] == ' ':
                            pygame.draw.rect(screen,red,pygame.Rect(x/10*10,y/10*10,10,10))
                            pygame.display.update()
                            end = (x/10 * 10, y/10 * 10)
                            maze[end[0]/10][end[1]/10] = 'F'

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if start and end:
            solver_algorithm(screen,maze)


visualize(20,20,depth_first_search,solve_maze_a_star)
