import math as m #provides the mathematical fuctions for the agent's movement equations.
import time
import pygame #for the simulation
import numpy as np #for numerical data manipulation
from src.game.sensor import Sensor

from src.utils.math_tools import get_distance
from src.common.constants import SimulationSettings

class Agent:

    deaths = 0

    def __init__(self, x, y, size, field_of_view, nb_sensors, max_range, brain):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
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
            brain_output = self.brain.forward([(sensor.distance / self.max_range) for sensor in self.sensors]) #QUESTION: why do we scale downn inputs to [0,1]?
            speed = brain_output[0]
            angle = brain_output[1]
            self.angle = np.interp(angle, [-1, 1], [-60, 60]) #linear interpolation is predicting a value from a set of predefined values using a linear equation https://www.youtube.com/watch?v=xwmcVd85VRE&t=26s
            #self.angle = 60*angle
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
                    if sensor.is_in_range(obstacle):
                        if obstacle not in sensor.obstacles_in_range:
                            sensor.obstacles_in_range.append(obstacle)
                        sensor.draw_closest_obstacle_interaction(screen, obstacle)
                    else:
                        #if it exist, remove obstacle from in_range obstacles
                        if obstacle in sensor.obstacles_in_range:
                            sensor.obstacles_in_range.remove(obstacle)
                        #if it's tured on, turn off the glowig interaction
                        if sensor.glowing and sensor.glowing_obstacle_id == obstacle.id:
                            sensor.turn_off()
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
            target_distance = get_distance((self.x, self.y), SimulationSettings.TARGET_LOCATION)
            if self.x <= 10 or self.y <= 10 or self.y >= SimulationSettings.HEIGHT - 20 \
                or self.x >= SimulationSettings.WIDTH - 20:
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
            distance_to_target = get_distance(robot_pos, SimulationSettings.TARGET_LOCATION)
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



