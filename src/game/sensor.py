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
        self.reading = self.max_range
        self.tag = tag
        self.x0 = self.x1 = self.y0 = self.y1 = 0
        self.origin = (self.x0,self.y0)
        self.end = (self.x1,self.y1)
        self.activated = False
        self.current_obstacle_id = None #serves to checks if the next detection is of the same obstacle or a new one
        self.engaged_obstacles = []

    def update(self):
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

    def detect_obstacle(self, screen, obstacle):

        intersection_point = obstacle.intersection_point(self)
        
        #check if the sensor is already engaged with an obstacle, and if it's different from the one it's reading now
        if self.current_obstacle_id and self.current_obstacle_id != obstacle.id:
            self._choose_closer_obstacle(obstacle)
        
        #if it's not already engaged 
        else:
            x_intersection, y_intersection = intersection_point
            self.reading = get_distance(self.origin, intersection_point)
            pygame.draw.line(screen, (255, 0, 0), (self.x0, self.y0), intersection_point)
            pygame.draw.circle(screen, (0, 255, 0), (int(x_intersection), int(y_intersection)), 1, 0) #indicates intersectionn point
            self.activated = True
            self.current_obstacle_id = obstacle.id

    def _choose_closer_obstacle(self, obstacle):
        intersection_point = obstacle.intersection_point(self)
        x_intersection, y_intersection = intersection_point
        new_reading = get_distance((self.x0, self.y0), (x_intersection, y_intersection))
        if new_reading < self.reading:
            self.current_obstacle_id = obstacle.id
            self.reading = new_reading

    def handle_obstacle_exit(self):
        """
        Resets sensor and the current obstacle variable
        when the obstacle that initially activated the sensor has disengaged.
        """
        if len(self.engaged_obstacles) > 1:
            readings = []
            for obstacle in self.engaged_obstacles:
                # find closest, set reading to that one
                coll = obstacle.intersection_point(self)
                if coll:
                    x_intersection, y_intersection = coll
                    distance = get_distance((self.x0, self.y0), (x_intersection, y_intersection))
                    readings.append(distance)
                    lowest_reading_idx = readings.index(min(readings))
                    self.reading = readings[lowest_reading_idx]
                    self.current_obstacle_id = None
        elif len(self.engaged_obstacles) == 1:
            # get distance of only obstacle set reading to that
            coll = self.engaged_obstacles[0].intersection_point(self)
            if coll:
                x_intersection, y_intersection = coll
                distance = get_distance((self.x0, self.y0), (x_intersection, y_intersection))
                self.reading = distance
                self.current_obstacle_id = None
        else:
            self.activated = False
            self.reading = self.max_range
            self.current_obstacle_id = None

    def in_range(self, obstacle):
        """
        Return true if the obstacle intersects with the sensor
        and false otherwise.
        """
        collision = obstacle.intersection_point(self)
        if collision:
            if obstacle not in self.engaged_obstacles:
                self.engaged_obstacles.append(obstacle)
            return True
        else:
            if obstacle in self.engaged_obstacles:
                self.engaged_obstacles.remove(obstacle)
            return False