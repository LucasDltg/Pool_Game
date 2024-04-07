import pygame
import sys
import pool
from color import *


window_size = [window_width, window_height] = [600, 600]
pygame.init()
screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)

pool_table = pool.Pool(window_size)

c = pygame.time.Clock()
while True:
    dt = c.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            window_size = [window_width, window_height] = [event.w, event.h]
            pool_table.handleResize(window_width, window_height)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            # change the position of the event to be relative to the pool table
            event.pos = (event.pos[0] - (window_width - pool_table.pool_table.get_width()) / 2,
                         event.pos[1] - (window_height - pool_table.pool_table.get_height()) / 2)
            pool_table.handleClick(event)

    # update game state
    pool_table.update(dt)

    # update screen
    screen.fill(black)
    pool_table.renderSurface(screen)

    pygame.display.flip()
