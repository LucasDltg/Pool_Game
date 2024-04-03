import pygame
import sys
import pool_1 as pool
from color import *

window_size = [window_width, window_height] = [600, 600]

pygame.init()
screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)

pool_table = pool.Pool(window_size)

c = pygame.time.Clock()
are_balls_moving = True
while True:
    dt = c.tick(120)/16.67
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            previous_size = pool_table.pool_table.get_size()
            window_size = [window_width, window_height] = [event.w, event.h]
            pool_table.Scale(previous_size, window_size)

    # update game state
    if are_balls_moving:
        are_balls_moving = pool_table.updateBalls(dt)

    #####################
    ##  update screen  ##
    #####################
    screen.fill(black)
    pool_surface = pool_table.pool_table.copy()
    # draw balls on table
    for b in pool_table.balls:
        pygame.draw.circle(pool_surface, b.color, (b.x_pos + b.size/2, b.y_pos + b.size/2), b.size/2)
        print(b.x_pos, b.y_pos, b.color)

    # draw table
    pool_table_size = pool_table.pool_table.get_size()
    screen.blit(pool_surface, ((window_size[0] - pool_table_size[0]) / 2, (window_size[1] - pool_table_size[1]) / 2))

    pygame.display.flip()


