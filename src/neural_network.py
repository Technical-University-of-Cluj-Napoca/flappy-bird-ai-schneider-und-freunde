import numpy as np
import random

class NeuralNetwork:
    """Simple feedforward neural network for the bird's brain"""
    
    def __init__(self, input_size=5, hidden_size=8, output_size=1):
        """
        Initialize neural network with random weights
        
        Inputs:
        - Bird Y position
        - Bird velocity
        - Next pipe X distance
        - Next pipe top Y
        - Next pipe bottom Y
        
        Output:
        - Jump decision (sigmoid > 0.5 = jump)
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # Initialize weights with Xavier initialization
        self.weights_input_hidden = np.random.randn(input_size, hidden_size) * np.sqrt(2.0 / input_size)
        self.bias_hidden = np.zeros((1, hidden_size))
        
        self.weights_hidden_output = np.random.randn(hidden_size, output_size) * np.sqrt(2.0 / hidden_size)
        self.bias_output = np.zeros((1, output_size))
    
    def sigmoid(self, x):
        """Sigmoid activation function"""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def relu(self, x):
        """ReLU activation function"""
        return np.maximum(0, x)
    
    def forward(self, inputs):
        """
        Forward propagation through the network
        
        Args:
            inputs: numpy array of shape (1, input_size)
        
        Returns:
            output: decision value (0-1)
        """
        # Input to hidden layer
        hidden = self.relu(np.dot(inputs, self.weights_input_hidden) + self.bias_hidden)
        
        # Hidden to output layer
        output = self.sigmoid(np.dot(hidden, self.weights_hidden_output) + self.bias_output)
        
        return output[0][0]
    
    def predict(self, bird_y, bird_velocity, pipe_x, pipe_top_y, pipe_bottom_y):
        """
        Make a decision whether to jump
        
        Args:
            bird_y: Current Y position of bird
            bird_velocity: Current velocity of bird
            pipe_x: X distance to next pipe
            pipe_top_y: Y position of top pipe bottom edge
            pipe_bottom_y: Y position of bottom pipe top edge
        
        Returns:
            bool: True if should jump, False otherwise
        """
        # Normalize inputs
        inputs = np.array([[
            bird_y / 512.0,  # Normalize by screen height
            (bird_velocity + 10) / 20.0,  # Normalize velocity
            pipe_x / 288.0,  # Normalize by screen width
            pipe_top_y / 512.0,
            pipe_bottom_y / 512.0
        ]])
        
        output = self.forward(inputs)
        return output > 0.5
    
    def copy(self):
        """Create a copy of this neural network"""
        new_nn = NeuralNetwork(self.input_size, self.hidden_size, self.output_size)
        new_nn.weights_input_hidden = self.weights_input_hidden.copy()
        new_nn.bias_hidden = self.bias_hidden.copy()
        new_nn.weights_hidden_output = self.weights_hidden_output.copy()
        new_nn.bias_output = self.bias_output.copy()
        return new_nn
    
    def mutate(self, mutation_rate=0.1, mutation_strength=0.5):
        """
        Mutate the neural network weights
        
        Args:
            mutation_rate: Probability of mutating each weight
            mutation_strength: Standard deviation of mutation
        """
        # Mutate input to hidden weights
        mask = np.random.random(self.weights_input_hidden.shape) < mutation_rate
        self.weights_input_hidden += mask * np.random.randn(*self.weights_input_hidden.shape) * mutation_strength
        
        # Mutate hidden to output weights
        mask = np.random.random(self.weights_hidden_output.shape) < mutation_rate
        self.weights_hidden_output += mask * np.random.randn(*self.weights_hidden_output.shape) * mutation_strength
        
        # Mutate biases
        mask = np.random.random(self.bias_hidden.shape) < mutation_rate
        self.bias_hidden += mask * np.random.randn(*self.bias_hidden.shape) * mutation_strength
        
        mask = np.random.random(self.bias_output.shape) < mutation_rate
        self.bias_output += mask * np.random.randn(*self.bias_output.shape) * mutation_strength
    
    def crossover(self, other):
        """
        Create a child network by crossing over with another network
        
        Args:
            other: Another NeuralNetwork instance
        
        Returns:
            NeuralNetwork: Child network
        """
        child = NeuralNetwork(self.input_size, self.hidden_size, self.output_size)
        
        # Crossover weights - random blend
        for i in range(self.weights_input_hidden.shape[0]):
            for j in range(self.weights_input_hidden.shape[1]):
                if random.random() < 0.5:
                    child.weights_input_hidden[i][j] = self.weights_input_hidden[i][j]
                else:
                    child.weights_input_hidden[i][j] = other.weights_input_hidden[i][j]
        
        for i in range(self.weights_hidden_output.shape[0]):
            for j in range(self.weights_hidden_output.shape[1]):
                if random.random() < 0.5:
                    child.weights_hidden_output[i][j] = self.weights_hidden_output[i][j]
                else:
                    child.weights_hidden_output[i][j] = other.weights_hidden_output[i][j]
        
        return child
