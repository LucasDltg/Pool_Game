import pygame
import sys
import pool
from color import *
import math

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
            pool_table.ScalePoolTable(window_size)
            pool_table.ScaleBalls(previous_size)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if not are_balls_moving:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    mouse_x -= (window_size[0] - pool_table_size[0]) / 2
                    mouse_y -= (window_size[1] - pool_table_size[1]) / 2

                    diff_x = mouse_x - (pool_table.balls[-1].x_pos + pool_table.balls[-1].size / 2)
                    diff_y = mouse_y - (pool_table.balls[-1].y_pos + pool_table.balls[-1].size / 2)

                    pool_table.balls[-1].x_speed = -0.01 * diff_x
                    pool_table.balls[-1].y_speed = -0.01 * diff_y
                    are_balls_moving = True

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

    # draw table
    pool_table_size = pool_table.pool_table.get_size()
    screen.blit(pool_surface, ((window_size[0] - pool_table_size[0]) / 2, (window_size[1] - pool_table_size[1]) / 2))

    # draw queue
    if not are_balls_moving:
        wball = (pool_table.balls[-1].x_pos + pool_table.balls[-1].size / 2 + (window_size[0] - pool_table_size[0]) / 2,
                 pool_table.balls[-1].y_pos + pool_table.balls[-1].size / 2 + (window_size[1] - pool_table_size[1]) / 2)
        mouse_pos = pygame.mouse.get_pos()

        direction_vector = (mouse_pos[0] - wball[0], mouse_pos[1] - wball[1])

        magnitude = math.sqrt(direction_vector[0] ** 2 + direction_vector[1] ** 2)
        if magnitude != 0:
            normalized_direction_vector = (direction_vector[0] / magnitude, direction_vector[1] / magnitude)
        else:
            normalized_direction_vector = (0, 0)

        desired_distance = pool_table.balls[-1].size * 1.5
        queue_size = pool_table_size[1]
        head_size = queue_size / 10

        p1 = (wball[0] + normalized_direction_vector[0] * desired_distance,
                         wball[1] + normalized_direction_vector[1] * desired_distance)
        p2 = (wball[0] + normalized_direction_vector[0] * queue_size,
                         wball[1] + normalized_direction_vector[1] * queue_size)
        p3 = (wball[0] + normalized_direction_vector[0] * head_size,
                         wball[1] + normalized_direction_vector[1] * head_size)

        pygame.draw.line(screen, brown_queue, p1, p2, width=2)
        pygame.draw.line(screen, (255, 255, 255), p1, p3, width=2)


    pygame.display.flip()


