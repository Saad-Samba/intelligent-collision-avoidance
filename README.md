# Collision Avoidance through Evolutionary Neural Network.

In this project, robots learn to avoid both static and dynamic obstacles, with no prior knowledge of the environment that they operate in. Each robot is controlled by a neural network with genetic algorithm. Over several generations, the robots achieve impressive behaviour.

## The Neural Network
The neural network contains an input layer composed of nine neurons that take distance to obstacle readings from the sensors of the robot, three hidden layers each consisting of sixteen neurons and two neurons at the output layer, controlling the speed and direction of the robot respectively.
For the activation function we have used either hyperbolic tanget or logit.

## The Genetic Algorithm
The algorithm passes through 6 main steps in order to produce an impressive agent at the task at hand, these are :
1. **Initialization** : We create a set of individuals with random genes which in our case are the neural network's weights. All of them will interact with the environment until an eventual death.
2. **Evaluation** : We evaluate each individual's performance using a fitness function once their lifespan ends. An intuitive choice of fitness function for this project could be, the closest distance that the robot achieved to the target during its lifetime.
3. **Selection** : Choose the fittest individuals, in this project we used two methods : truncation and roulette wheel.
4. **Crossover** : From the selected individuals, we choose two that will combine their genes to produce a child. In this project we used Uniform Crossover, which chooses randomly a gene from one of the parents.
5. **Mutation** : Randomly modifies the child's gees with the purpose of injecting genetic diversity into the population.
6. **Termination** :  We loop over the previous 3 steps until we get a new generation with same the number of individuals.




# The Simulation
<img src="images/demo.gif" width="750">

This simulation is built using the 2d game library Pygame. The simulation is simple, it can be thought of as a map, a thin white border marks the boundary of the map. The goal of the robot is to reach a small red target which is obstructed by some obstacle, such that the only way to reach the target is to avoid/manoeuvre around it.

The robot's lifespan ends when one of three conditions is met:
* The robot collides with an obstacle
* The robot collides with the boundaries of the map
* The time that the robot is alive exceeds a preset threshold : to prevent a situation where the robot achieves a speed of zero indefinitely and is therefore unable to move.
* The robot collides with the target.









