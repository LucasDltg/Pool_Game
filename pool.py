import ball
import pygame
from color import *
import math


class Pool:

    def __init__(self, size: list[int]):
        self.pool_table: pygame.Surface = None
        self.balls: list[ball.Ball] = []
        self.width, self.height = 0, 0
        self.borders = []   # (X, Y)
        self.holes = []     # (centerX, centerY, radius)

        self.ScalePoolTable(size)
        self.InitBalls()

    def InitBalls(self) -> None:
        """
        Initialise the position of the balls
        :return:
        """
        colors = [red, red, yellow, yellow, black, red, red, yellow, red, yellow, yellow, red, yellow, yellow, red]
        diameter = self.height / 26

        y = self.height / 2 - diameter / 2  # middle of the table
        x = self.width / 4
        color_idx = 0
        dy = [0, -0.5, 0.5, -1, 0, 1, -1.5, -0.5, 0.5, 1.5, -2, -1, 0, 1, 2]

        for i in range(5):
            for j in range(i + 1):
                self.balls.append(ball.Ball(x, y + dy[color_idx] * diameter, size=diameter, color=colors[color_idx]))
                color_idx += 1
            x -= diameter
        self.balls.append(ball.Ball(self.width * 3 / 4, self.height / 2 - diameter / 2, -10, 0, size=diameter, color=(255, 255, 255)))

    def ScaleBalls(self, previous_size) -> None:
        radius = self.height / 26
        for b in self.balls:
            b.x_pos = b.x_pos / previous_size[0] * self.width
            b.y_pos = b.y_pos / previous_size[1] * self.height
            b.size = radius
            b.x_speed = b.x_speed / previous_size[0] * self.width
            b.y_speed = b.y_speed / previous_size[1] * self.height

    def ScalePoolTable(self, window_size) -> None:
        width = window_size[0] * 8 / 10
        height = width * 9 / 16
        border_size = height * 1 / 16
        border_radius = int(border_size / 4 * 3)
        band_width = int(border_size / 4)
        hole_diameter = height / 16  # same as border size
        hole_offset = 1
        plate_size = border_size + hole_diameter / 3 * 2

        self.pool_table = pygame.surface.Surface((width, height))
        self.width = width
        self.height = height

        # draw border
        pygame.draw.rect(self.pool_table, brown, pygame.Rect(0, 0, width, height), border_radius=border_radius)

        # draw metal plate under holes
        pygame.draw.rect(self.pool_table, gray_angle, pygame.Rect(0, 0, plate_size, plate_size),
                         border_top_left_radius=border_radius)
        pygame.draw.rect(self.pool_table, gray_angle, pygame.Rect((width - plate_size) / 2, 0, plate_size, border_size))
        pygame.draw.rect(self.pool_table, gray_angle, pygame.Rect(width - plate_size, 0, plate_size, plate_size),
                         border_top_right_radius=border_radius)
        pygame.draw.rect(self.pool_table, gray_angle, pygame.Rect(0, height - plate_size, plate_size, plate_size),
                         border_bottom_left_radius=border_radius)
        pygame.draw.rect(self.pool_table, gray_angle,
                         pygame.Rect((width - plate_size) / 2, height - border_size, plate_size, border_size))
        pygame.draw.rect(self.pool_table, gray_angle,
                         pygame.Rect(width - plate_size, height - plate_size, plate_size, plate_size),
                         border_bottom_right_radius=border_radius)
        pygame.draw.rect(self.pool_table, green_pool,
                         pygame.Rect(border_size, border_size, width - border_size * 2, height - border_size * 2))

        # draw bands
        # in order: top left, top right, left, right, bottom left, bottom right
        # points are in anti-clockwise order with the useless border in last

        # all the possibles values of x in ascending order
        x1 = border_size
        x2 = border_size + band_width
        x3 = border_size + hole_diameter / 2
        x4 = border_size + hole_diameter / 2 + band_width
        x5 = (width - hole_diameter) / 2 - band_width / 2
        x6 = (width - hole_diameter) / 2
        x7 = (width + hole_diameter) / 2
        x8 = (width + hole_diameter) / 2 + band_width / 2
        x9 = width - border_size - hole_diameter / 2 - band_width
        x10 = width - border_size - hole_diameter / 2
        x11 = width - border_size - band_width
        x12 = width - border_size

        y1 = border_size
        y2 = border_size + band_width
        y3 = border_size + hole_diameter / 2
        y4 = border_size + hole_diameter / 2 + band_width
        y5 = height - border_size - hole_diameter / 2 - band_width
        y6 = height - border_size - hole_diameter / 2
        y7 = height - border_size - band_width
        y8 = height - border_size

        points = [(x3, y1), (x4, y2), (x5, y2), (x6, y1)]
        points += [(x7, y1), (x8, y2), (x9, y2), (x10, y1)]
        points += [(x1, y6), (x2, y5), (x2, y4), (x1, y3)]
        points += [(x12, y3), (x11, y4), (x11, y5), (x12, y6)]
        points += [(x6, y8), (x5, y7), (x4, y7), (x3, y8)]
        points += [(x10, y8), (x9, y7), (x8, y7), (x7, y8)]

        self.borders = points

        pygame.draw.polygon(self.pool_table, green_band, points[:4])
        pygame.draw.polygon(self.pool_table, green_band, points[4:8])
        pygame.draw.polygon(self.pool_table, green_band, points[8:12])
        pygame.draw.polygon(self.pool_table, green_band, points[12:16])
        pygame.draw.polygon(self.pool_table, green_band, points[16:20])
        pygame.draw.polygon(self.pool_table, green_band, points[20:24])

        # draw holes
        holes = [(border_size + hole_offset, border_size + hole_offset, hole_diameter / 2),
                 (width / 2, border_size - hole_offset, hole_diameter / 2),
                 (width - border_size - hole_offset, border_size + hole_offset, hole_diameter / 2),
                 (border_size + hole_offset, height - border_size - hole_offset, hole_diameter / 2),
                 (width / 2, height - border_size + hole_offset, hole_diameter / 2),
                 (width - border_size - hole_offset, height - border_size - hole_offset, hole_diameter / 2)]

        self.holes = holes

        pygame.draw.circle(self.pool_table, black, holes[0][:2], holes[0][2])
        pygame.draw.circle(self.pool_table, black, holes[1][:2], holes[1][2])
        pygame.draw.circle(self.pool_table, black, holes[2][:2], holes[2][2])
        pygame.draw.circle(self.pool_table, black, holes[3][:2], holes[3][2])
        pygame.draw.circle(self.pool_table, black, holes[4][:2], holes[4][2])
        pygame.draw.circle(self.pool_table, black, holes[5][:2], holes[5][2])

    def updateBalls(self, dt) -> bool:
        """
        Update balls position by resolving ball-ball collision, ball-wall collision, ball-hole collision and friction
        :return: True is balls are moving, false otherwise
        """
        ret = False
        for i in range(len(self.balls)):

            # collision with border
            for j in range(len(self.borders)):
                # because borders are made of 4 points and we skip the useless border
                if (j - 3) % 4 == 0:
                    continue

                x1, y1 = self.borders[j]
                x2, y2 = self.borders[(j + 1) % len(self.borders)]  # Wrap around to the first point
                collision = self.detectCollision(i, self.balls[i].x_pos + self.balls[i].size / 2,
                                                 self.balls[i].y_pos + self.balls[i].size / 2,
                                                 self.balls[i].size/2, x1, y1, x2, y2)

                if collision:
                    new_x_pos, new_y_pos, new_x_speed, new_y_speed = collision
                    self.balls[i].x_pos = new_x_pos - self.balls[i].size / 2
                    self.balls[i].y_pos = new_y_pos - self.balls[i].size / 2
                    self.balls[i].x_speed = new_x_speed
                    self.balls[i].y_speed = new_y_speed
                    break

            # collision between balls
            for j in range(i + 1, len(self.balls)):
                if self.balls[i].isColliding(self.balls[j], dt):
                    self.balls[i].resolveCollision(self.balls[j], dt)

            # collision with holes
            for hole in self.holes:
                hole_x, hole_y, hole_radius = hole
                dist_squared = (self.balls[i].x_pos + self.balls[i].size/2 - hole_x) ** 2 + (self.balls[i].y_pos + self.balls[i].size/2 - hole_y) ** 2
                if dist_squared <= hole_radius ** 2:
                    # Ball fell into the hole, remove it or update its position
                    self.balls[i].size -= 1
                    self.balls[i].x_pos = hole_x - self.balls[i].size/2
                    self.balls[i].y_pos = hole_y - self.balls[i].size/2


                    if self.balls[i].size <= 0:
                        self.balls[i].x_pos = -1
                        self.balls[i].y_pos = -1
                    break

            friction_coefficient = 0.01 * dt
            self.balls[i].x_speed -= self.balls[i].x_speed * friction_coefficient
            self.balls[i].y_speed -= self.balls[i].y_speed * friction_coefficient
            self.balls[i].x_pos += self.balls[i].x_speed * dt
            self.balls[i].y_pos += self.balls[i].y_speed * dt

            if abs(self.balls[i].x_speed) < 1e-1 and abs(self.balls[i].y_speed) < 1e-1:
                self.balls[i].x_speed = 0
                self.balls[i].y_speed = 0
            else:
                ret = True
        return ret

    def detectCollision(self, i, ball_x, ball_y, ball_radius, line_x1, line_y1, line_x2, line_y2):
        """
        detect collision between self.balls[i] and self.borders
        :param i: ball concerned
        :param ball_x:
        :param ball_y:
        :param ball_radius:
        :param line_x1:
        :param line_y1:
        :param line_x2:
        :param line_y2:
        :return:
        """
        # Calculate the vector from one end of the line segment to the ball
        vec_line_to_ball = [ball_x - line_x1, ball_y - line_y1]

        # Calculate the vector representing the line segment
        vec_line = [line_x2 - line_x1, line_y2 - line_y1]

        # Calculate the projection of vec_line_to_ball onto vec_line
        dot_product = vec_line_to_ball[0] * vec_line[0] + vec_line_to_ball[1] * vec_line[1]
        vec_line_squared_length = vec_line[0] * vec_line[0] + vec_line[1] * vec_line[1]

        if dot_product < 0:
            # Ball is beyond the start of the line segment
            closest_point = [line_x1, line_y1]
        elif dot_product > vec_line_squared_length:
            # Ball is beyond the end of the line segment
            closest_point = [line_x2, line_y2]
        else:
            # Ball is within the bounds of the line segment
            projection_scale = dot_product / vec_line_squared_length
            closest_point = [line_x1 + vec_line[0] * projection_scale,
                             line_y1 + vec_line[1] * projection_scale]

        # Check if the closest point is within the ball's radius
        distance_squared = (ball_x - closest_point[0]) ** 2 + (ball_y - closest_point[1]) ** 2
        if distance_squared <= ball_radius ** 2:
            # Collision detected, calculate new ball position and velocity
            normal = [ball_x - closest_point[0], ball_y - closest_point[1]]
            normal_length = math.sqrt(normal[0] ** 2 + normal[1] ** 2)
            normal[0] /= normal_length
            normal[1] /= normal_length
            dot_product = self.balls[i].x_speed * normal[0] + self.balls[i].y_speed * normal[1]
            new_speed_x = self.balls[i].x_speed - 2 * dot_product * normal[0]
            new_speed_y = self.balls[i].y_speed - 2 * dot_product * normal[1]
            new_x_pos = closest_point[0] + normal[0] * ball_radius
            new_y_pos = closest_point[1] + normal[1] * ball_radius
            return new_x_pos, new_y_pos, new_speed_x, new_speed_y

        return None
