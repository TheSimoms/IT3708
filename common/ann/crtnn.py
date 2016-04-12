from numpy import array, add

from common.ann.utils import sigmoid_function


class BiasNeuron:
    def __init__(self, value):
        self.y = value

    @property
    def output_value(self):
        return self.y


class NormalNeuron:
    def __init__(self):
        self.y = 0

        self.s = None
        self.gains = None
        self.time = None

    def set_input(self, value):
        self.s = value
        self.y = self.y + (self.s - self.y) / self.time

    @property
    def output_value(self):
        return sigmoid_function(self.gains * self.y)


class ContinuousTimeRecurrentNeuralNetwork:
    def __init__(self, layers):
        self.layers = layers

        self.looping_connections = None
        self.intra_connections = None

    def fill_layer(self, i, values):
        for j, value in enumerate(values):
            self.layers[i][j].set_input(values)

    def get_layer_values(self, i, is_bias=True):
        if is_bias:
            return array([neuron.output_value for neuron in self.layers[i]])

        return array([neuron.output_value for neuron in self.layers[i] if isinstance(neuron, NormalNeuron)])

    def get_number_of_neurons_in_layer(self, i):
        return (
            sum(isinstance(neuron, NormalNeuron) for neuron in self.layers[i]),
            sum(isinstance(neuron, NormalNeuron) for neuron in self.layers[i]),
        )

    def apply_phenotype(self, phenotype):
        self.looping_connections = phenotype['looping_connections']
        self.intra_connections = phenotype['intra_connections']

        i = 0

        for layer in self.layers:
            for neuron in layer:
                if isinstance(neuron, NormalNeuron):
                    i += 1

                    neuron.gains = phenotype['gains'][i]
                    neuron.time = phenotype['time'][i]

    def run_input_values(self, input_values):
        self.fill_layer(0, input_values)

        for i in range(len(self.layers) - 1):
            self.fill_layer(
                i + 1,
                add(
                    self.get_layer_values(i + 1, is_bias=False).dot(self.looping_connections[i]),
                    self.get_layer_values(i).dot(self.intra_connections[i])
                )
            )
