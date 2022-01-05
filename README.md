# Collision Avoidance through Evolutionary Neural Network.

In this project, agents learn to avoid both static and dynamic obstacles, with no prior knowledge of the environment that they operate in. Each robot is controlled by a neural network with an optimization algorithm called genetic algorithm. Over several generations, the robots achieve impressive behaviour.

<img src="images/demo.gif" width="750">

## The Genetic Algorithm
The algorithm passes through 6 main steps in order to produce an impressive agent at the task at hand, these are :
1. **Initialization** : We create a set of individuals with random traits. All of them will interact with the environment until an eventual death.
2. **Evaluation** : We evaluate each individual's performance using a fitness function. An intuitive choice of fitness function for this project could be, the closest distance that the robot achieved to the target during its lifetime.
3. **Selection** : Choose the fittest individuals, in this project we used two methods : truncation and roulette wheel.
4. **Crossover** : From the selected individuals, we choose two that will combine their genes to produce a child. In this project we used Uniform Crossover, which chooses randomly a gene from one of the parents.
<img src="images/Uniform Crossover.png" width="750">
5. **Mutation** : Randomly modifies the child's gees with the purpose of injecting genetic diversity into the population.
6. **Termination** :  We loop over the previous 3 steps until we get a new generation with same the number of individuals.

# The Simulation

This simulation is built using the 2d python game framework Pygame. The simulation is simple, it can be thought of as a map, a thin white border marks the boundary of the map. The goal of the robot is to reach a small red target which is obstructed by some obstacle, such that the only way to reach the target is to avoid/manoeuvre around it.

The robot's lifespan ends when one of three conditions is met:
* The robot collides with an obstacle
* The robot collides with the boundaries of the map
* The time that the robot is alive exceeds a preset threshold
* The robot collides with the target

The third condition is put in place to prevent a situation where the robot achieves a speed of zero indefinitely and is therefore unable to move. The threshold is set such that is larger than the time required for successfully reaching the target. This means that it should only eliminate robots that get stuck.

The fourth and final conditions can be considered as the robot successfully achieving the desired goal of reaching the target.

#### Static Case
In this project, two scenarios are tackled the first of which being a static case. This involves two stationary obstacles placed one after another and before the target. The robot's then spawn before the obstacle with the goal of reaching the target.

#### Dynamic Case
The dynamic scenario consists of a single obstacle which continuously moves up and down in a linear reciprocating motion with the target on the other side of the obstacle. This is much tougher since even if the robot is successful on a single attempt, this does not mean that it will succeed in future attempts as the obstacle may be in a different position which causes problems.

## The Robot

The robot has nine sensors which are placed around its circumference and equally spaced. These sensors measure distance to any nearby obstacles, and it is these sensor readings that serve as input to the neural network. The neural network then outputs two continuous values, one controlling the speed and the other controlling the direction of the robot. This process happens continuously all the time the robot is alive. It is these sensors that give the robot reactive behaviour - that is based on changing sensor readings the robot can adjust its speed and direction in real time. As a pose to similar project involving genetic algorithms which use a preselected set of direction vectors to map an agent's trajectory.


## The Neural Network
The Neural network used in this project is a vanilla feed forward neural network. It contains nine input neurons, since it takes readings from the nine sensor readings provided from the robot, three hidden layers each consisting of sixteen neurons, and an output layer consisting of two neurons, controlling the speed and direction of the robot respectively.


## Combining a Neural Network and Genetic Algorithm
At this stage, you may be wondering how the two are related in this project. The neural networks weights essentially represent the candidate solution itself, and its these numerical values of the weights that the genetic algorithm operates on directly.









