import math as m #provides the mathematical fuctions for the agent's movement equations.
import time
import pygame #for the simulation
import numpy as np #for numerical data manipulation
from src.game.sensor import Sensor

from src.utils.math_tools import get_distance
'''The first function calculate the intersection point between the sensor and a rectangle obstacle.
   The second computes the distance between two points.
'''
from src.common.constants import GameSettings #The settings for the game and the agent

class Agent:
    """
    This class defines the intelligent agent for this project and handles it's
    primary functions such as movement, visual updates, interfacing with sensors,
    fitness evaluation and dying.
    """
    deaths = 0

    def __init__(self, x, y, size, field_of_view, nb_sensors, max_range, brain):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        #The 3 parameters are found in constants.AgentSettings
        self.size = size
        self.colour = (255, 255, 255)
        self.max_range = max_range
        self.sensors = []
        self.angle = 0  # agent's orientation
        self.base_speed = 6
        self.alive = True
        self.brain = brain
        self.fitness = 0
        self.time_alive = time.time() #gives the birth date of the child.
        self.hit_target = False  #Boolean that indicates if our agent has ever reached the destination.
        self.best_distance = 1e6 #why is the distace 1e6?
        self._attach_sensors(field_of_view, nb_sensors, max_range)
    
    def move(self):
        """
        Handles the movement of the agent based on the output of the neural network.
        The neural network outputs two values based on the sensor reading inputs.
        One output controls the speed and the other controls the direction.
        """
        if self.alive:
            brain_output = self.brain.forward(
                [(sensor.distance / self.max_range) for sensor in self.sensors])
            speed = brain_output[0]
            angle = brain_output[1]
            self.angle = np.interp(angle, [-1, 1], [-60, 60])
            self.x += self.base_speed * speed * (m.cos(m.radians(self.angle)))
            self.y += self.base_speed * speed * (m.sin(m.radians(self.angle)))

    def update(self, screen, obstacles):
        """
        Responsible for drawing the agent onto the screen after it's position
        has been updated by the move function. Also check's if the agent has been
        alive longer than a specified threshold and kills it if it has.
        """
        if self.alive:
            pygame.draw.circle(screen, self.colour,
                               (int(self.x), int(self.y)), self.size, 0)
            for sensor in self.sensors:
                sensor.move()
                sensor.draw_indicators(screen)
                for obstacle in obstacles:
                    self._collide(obstacle)
                    if sensor.in_range(obstacle):
                        sensor.detect_obstacle(screen, obstacle)
                    else:
                        if sensor.activated and sensor.current_obstacle_id == obstacle.id:
                            sensor.handle_obstacle_exit()
        if self.alive:
            if time.time() - self.time_alive > 6:
                self.alive = False
                Agent.deaths += 1

    def _collide(self, obstacle):
        """
        Checks for collision between the agent and the obstacle, or
        between agent and map boundary. If there is a collision, the agent is killed.
        """
        if self.alive:
            target_distance = get_distance((self.x, self.y), GameSettings.TARGET_LOCATION)
            if self.x <= 10 or self.y <= 10 or self.y >= GameSettings.HEIGHT - 20 \
                or self.x >= GameSettings.WIDTH - 20:
                self.alive = False
                Agent.deaths += 1
            if obstacle.collide(self):
                self.alive = False
                Agent.deaths += 1
            if target_distance <= self.size + 10:
                self.alive = False
                self.hit_target = True
                Agent.deaths += 1

    def evaluate_fitness(self):
        """
        Scores the agent based on how well it performed on the task.
        """
        if self.alive:
            robot_pos = (self.x, self.y)
            distance_to_target = get_distance(robot_pos, GameSettings.TARGET_LOCATION)
            if distance_to_target < self.best_distance:
                self.best_distance = distance_to_target
            target_factor = 1 if self.hit_target else 0
            self.fitness = (1 / distance_to_target) + 0.5 * (1 / self.best_distance) \
                + 0.3 * target_factor

    def _attach_sensors(self, field_of_view, nb_sensors, max_range):
        interval = field_of_view / nb_sensors
        angle = 0
        for i in range(nb_sensors):
            self.sensors.append(Sensor(self, angle, max_range, i))
            angle += interval



