import numpy as np #Library for Numerical Data Manipulation


class NeuralNetwork: #Vanilla feedforward architecture.

    def __init__(self, inputs, hidden_layers, hidden_units, outputs, new_weights=False):
        self.inputs = inputs #number of neurons in the input layer
        self.hidden_layers = hidden_layers #number of hidden layers
        self.hidden_units = hidden_units #number of neuros in a hidden layer with all the hidden layers having the same number.
        self.outputs = outputs #number of units in the output layer
        if new_weights:
            self.weights = new_weights #provide weights
        else:
            self.weights = self._create_weights() #generate random weights

    def _create_weights(self):
        """
        Each weights between two consecutive layers can be represented in a matrix, 2-d np array.
        The function then returns a list of matrices which serve as the starting weights
        for the neural network, these weights are initialised randomly
        from a normal distribution with mean 0.
        """
        w_first = np.random.randn(self.inputs, self.hidden_units)
        w_last = np.random.randn(self.hidden_units, self.outputs)
        weights = [w_first]
        for _ in range(self.hidden_layers - 1):
            weights.append(np.random.randn(
                self.hidden_units, self.hidden_units))
        weights.append(w_last)
        return weights

    def _activation(self, z, tan_1=True): # Activation function : hyperbolic tanget or logit.

        if tan_1:
            return np.tanh(z) #hyperbolic tangent
        else:
            return 1 / (1 + np.exp(-z)) #logistic

    def forward(self, initial_x): #Forward propagation

        new_x = self._activation(np.dot(initial_x, self.weights[0]))
        for i in self.weights[1:]:
            new_x = np.dot(new_x, i)
            new_x = self._activation(new_x)
        return new_x


    def convert_weights_to_genome(self):
        """
        Takes the weights of the network as a list of matrices
        and converts them into a single vector. (a genome)
        The goal is to prepare parent agents for crossover.
        """
        flattened_weights = [w.flatten() for w in self.weights] #return a list of vector
        genome = np.concatenate(flattened_weights) #return one vector
        return genome
    def convert_genome_to_weights(self, genome):
        """
        Takes a vector, the genome, and reshapes it into the a list of
        matrices.
        """
        shapes = [np.shape(w) for w in self.weights] #shape is a tuple that contains the length of the columns and rows (N,M)
        products = [i[0]*i[1] for i in shapes] #retruns the number of elements in the matric, which is NxM
        weights = []
        start_idx = 0
        for i in range(len(products)):
            stop_idx = sum(products[:i+1]) #the position of the last weight of a matrix
            weight = np.reshape(genome[start_idx:stop_idx], shapes[i])
            weights.append(weight)
            start_idx += products[i] #the position of the first weight of a matrix
        return weights
