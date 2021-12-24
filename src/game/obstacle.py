import pygame

from src.utils.math_tools import circle_line_intersection, get_distance

class Circle:
    """
    Circle class which serves as an obstacles.
    """
    def __init__(self, x, y, r, colour, id):
        self.x = x
        self.y = y
        self.r = r
        self.colour = colour
        self.id = id
        self.reached_top = False
        self.reached_bottom = False
        self.direction = 1

    def draw(self, screen):
        """
        Draws the circle on to the screen.
        """
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.r, 0)

    def collide(self, agent):
        """
        Returns True if the agent has collided with the circle
        and False otherwise.
        """
        distance = get_distance((self.x, self.y), (agent.x, agent.y))
        return distance**2 < (self.r + agent.size)**2

    def intersect(self, sensor):
        """
        Computes the intersection, if any, between a line segment and
        and the circle obstacle.
        """
        intersection_pts = circle_line_intersection(
            (sensor.x0, sensor.y0),
            (sensor.x1, sensor.y1),
            (self.x, self.y),
            self.r
        )
        return intersection_pts

    def move(self):
        """
        Makes the circle oscillate back and forth in the y
        axis.
        """
        if self.y > 450 and not self.reached_bottom:
            self.direction *= -1
            self.reached_top = False
            self.reached_bottom = True

        if self.y < 150 and not self.reached_top:
            self.direction *= -1
            self.reached_top = True
            self.reached_bottom = False
        self.y += 0.5 * self.direction

