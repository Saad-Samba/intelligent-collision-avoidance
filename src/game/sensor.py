import pygame
import math as m

from src.utils.math_tools import get_distance




class Sensor:
    """
    Sensors that the agent uses to detect distance
    to nearby obstacles. The sensors in this project
    are represented as straight line segments with origin and end coordinates of
    (x0, y0) and (x1, y1) respectively. We the rely on mathematical functions to
    determine the distance and intersection points.
    """

    def __init__(self, agent, angle, max_range, tag):
        self.agent = agent
        self.angle = angle
        self.max_range = max_range
        self.distance = self.max_range
        self.tag = tag
        self.x0 = self.x1 = self.y0 = self.y1 = 0
        self.origin = (self.x0, self.y0)
        self.end = (self.x1, self.y1)
        self.activated = False
        self.current_obstacle_id = None #serves to checks if the next detection is of the same obstacle or a new one
        self.obstacles_in_range = [] #list all obstacles in range of the sensor

    def move(self):
        """
        Updates the position of the sensor in accordance with the position of the agent,
        such that the sensor is always 'attached' to the body of the agent.
        """
        self.x0 = self.agent.x + self.agent.size * \
            m.cos(m.radians(self.angle + self.agent.angle))
        self.y0 = self.agent.y + self.agent.size * \
            m.sin(m.radians(self.angle + self.agent.angle))
        self.x1 = self.agent.x + (self.agent.size + self.max_range) * \
            m.cos(m.radians(self.angle + self.agent.angle))
        self.y1 = self.agent.y + (self.agent.size + self.max_range) * \
            m.sin(m.radians(self.angle + self.agent.angle))
        self.origin = (self.x0, self.y0)
        self.end = (self.x1, self.y1)


    def draw_indicators(self, screen):
        """
        Draws one line that is an extension of a sensor to give a visual indication of the robot orientation.
        You can change which sensor by choosing a number from 0 to Number_Sensors, but it doesn't matter which one.
        """
        if self.tag == 0:
            pygame.draw.line(screen, (0, 0, 0), (self.agent.x, self.agent.y), (self.x0, self.y0))

        """
        Display end points of the sensor. (uncomment to see)
        """
        #if not self.activated:
             #pygame.draw.circle(screen, (0, 255, 0), (int(self.x1), int(self.y1)), 1, 0)


    def draw_closest_obstacle_interaction(self, screen, obstacle):

        '''
        Displays the line segment part with the closer obstacle.
        if :
        checks if the current obstacle id contains the id of the closest obstacle and handles it if not.
        Keeps doing it until he reaches the other condition.
        else :
        takes the obstacle's id, activates the sensor, draws its line and intersection point.
        '''

        intersection_point = obstacle.intersection_point(self)

        if self.current_obstacle_id and self.current_obstacle_id != obstacle.id:
            self._choose_closer_obstacle(obstacle)

        else:
            self.current_obstacle_id = obstacle.id
            self.activated = True
            self.distance = get_distance(self.origin, intersection_point)
            pygame.draw.line(screen, (255, 0, 0), self.origin, intersection_point)
            pygame.draw.circle(screen, (0, 255, 0), intersection_point, 1, 0) #indicates intersectionn point


    def _choose_closer_obstacle(self, obstacle):
        intersection_point = obstacle.intersection_point(self)
        new_distance = get_distance((self.x0, self.y0), intersection_point)
        if new_distance < self.distance:
            self.current_obstacle_id = obstacle.id
            self.distance = new_distance


    def handle_obstacle_exit(self):
        """
        Resets sensor and the current obstacle variable
        when the obstacle that initially activated the sensor has disengaged.
        """
        if len(self.obstacles_in_range) > 1:
            distances = []
            for obstacle in self.obstacles_in_range:
                # find closest, set distance to that one
                intersection_point = obstacle.intersection_point(self)
                if intersection_point:
                    distance = get_distance(self.origin, intersection_point)
                    distances.append(distance)
                    lowest_reading_idx = distances.index(min(distances))
                    self.distance = distances[lowest_reading_idx]
                    self.current_obstacle_id = None
        elif len(self.obstacles_in_range) == 1:
            # get distance of only obstacle set reading to that
            intersection_point = self.obstacles_in_range[0].intersection_point(self)
            if intersection_point:
                x_intersection, y_intersection = intersection_point
                distance = get_distance((self.x0, self.y0), (x_intersection, y_intersection))
                self.distance = distance
                self.current_obstacle_id = None
        else:
            self.activated = False
            self.distance = self.max_range
            self.current_obstacle_id = None

    def is_in_range(self, obstacle):
        """
        Return true if the obstacle is in range and false otherwise.
        """
        intersection_point = obstacle.intersection_point(self)
        if intersection_point:
            return True
        else:
            return False