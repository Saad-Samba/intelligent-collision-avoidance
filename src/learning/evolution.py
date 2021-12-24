import random
from bisect import bisect_left
from itertools import accumulate

from src.common.constants import AgentSettings, NeuralNetworkSettings
from src.game.agent import Agent
from src.learning.neural_network import NeuralNetwork


class Evolution: # Applies the genetic algorithm which will evolve the agents towards a successful solution.


    def __init__(self, population, elitism, mutation_rate, population_size):
        self.population = population #list of robots
        self.elitism = elitism #a value that decided the number of robots to take starting from the best and going downward.
        self.mutation_rate = mutation_rate #a value that controls the probability of a certain weight of the new born to be changed
        self.population_size = population_size
        self.generation = 0
        self.best_fitness = 0 #?

    def check_if_all_dead(self): #Checks if a generation died.

        if Agent.deaths >= len(self.population):
            return True
        return False


    def make_next_generation(self):
        """
        Creates the next generation, by repeatedly selecting parents,
        creating a child until n children have been created where
        n is the population size.
        """
        cumulative_fitness = self._get_cumulative_fitness()
        next_generation = []
        for _ in range(self.population_size):
            parent_one = self._truncation_selection()
            parent_two = self._truncation_selection()
            # parent_one = self._roulette_wheel_selection(cumulative_fitness)
            # parent_two = self._roulette_wheel_selection(cumulative_fitness)
            child = self._create_child(parent_one, parent_two)
            next_generation.append(child)
        Agent.deaths = 0
        self.population = next_generation


    def _truncation_selection(self):
        """
        Only the agents among the n fittest will have a change to be chosen
        where x is the elitism value
        """
        self.population.sort(key=lambda x: x.fitness)
        fittest = self.population[-self.elitism:]
        return random.choice(fittest)


    def _roulette_wheel_selection(self, cumulative_fitness):
        """
        It chooses a random number between 0 and 1,
        inserts it in the list of cumulative_fitness in a way to preserve the order, then it takes the first cumulative_fitness
        value just right to it and returns it's agent (parent_index).
        Every agent has the chance to be chosen.
        Only that the bigger it's fitness value the bigger it's probability to be chosen.
        ( because the bigger its fitness the bigger the interval between its according accumulative_value and the previous one)
        """
        parent_index = bisect_left(
            cumulative_fitness, random.uniform(0,1))

        return self.population[parent_index]
    def _get_cumulative_fitness(self):
        """
        Returns the cumulative fitness of the population,
        these are then treated as the probability for selection
        of each robot in the roulette wheel selection strategy.
        """
        self.population.sort(key=lambda x: x.fitness)
        fitness_values = [p.fitness for p in self.population]
        relative_fitness_values = [(f / sum(fitness_values)) for f in fitness_values]
        cumulative_fitness = list(accumulate(relative_fitness_values))
        return cumulative_fitness


    def _create_host_agent(self, weights):
        """
        Creates a new agent of the same population only with weights
        passed as an argument which will be the weights taken from the parents.
        """
        brain = NeuralNetwork(
            inputs=NeuralNetworkSettings.INPUT_UNITS,
            hidden_layers=NeuralNetworkSettings.HIDDEN_LAYERS,
            hidden_units=NeuralNetworkSettings.HIDDEN_UNITS,
            outputs=NeuralNetworkSettings.OUTPUTS,
            new_weights=weights
        )
        agent = Agent(
            x=AgentSettings.START_X,
            y=AgentSettings.START_Y,
            size=AgentSettings.SIZE,
            field_of_view=AgentSettings.FIELD_OF_VIEW,
            nb_sensors=AgentSettings.NB_SENSORS,
            max_range=AgentSettings.MAX_RANGE,
            brain=brain
        )
        return agent


    def _create_child(self, first_parent, second_parent):
        """
        Takes two parents and creates a child by applying uniform crossover
        to their genes.
        """
        child_genome = []
        first_parent_genome = first_parent.brain.convert_weights_to_genome()
        second_parent_genome = second_parent.brain.convert_weights_to_genome()
        for i in range(len(first_parent_genome)):
            if random.random() > 0.5: #returns a random number between 0 and 1
                child_genome.append(first_parent_genome[i])
            else:
                child_genome.append(second_parent_genome[i])
        self._mutate(child_genome)
        child_weights = first_parent.brain.convert_genome_to_weights(child_genome) 
        """i wondered why exactly chose first parent, then I figured this function is actually 
        independent of the agent, it's just a mathematical function that converts a vector 
        to an array, which means we can even get it out of the class Neural Network"""
        return self._create_host_agent(child_weights)
    def _mutate(self, genome):
        """
        Iterates through the genome of a new born with a probability
        related to the mutation rate to change a gene.
        """
        for i in range(len(genome)):
            if random.random() < self.mutation_rate:
                genome[i] = random.gauss(0, 1) #normal distribution

