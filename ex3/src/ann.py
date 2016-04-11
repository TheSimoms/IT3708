from numpy import concatenate, zeros, vectorize, array


class ANN:
    def __init__(self, layers, activation_function, activation_threshold=0.0, bias=None):
        if bias is None:
            bias = {}

        self.layers = layers
        self.bias = bias

        self.relations = None
        self.neurons = [
            concatenate(
                (zeros(layer_size), self.bias.get(i, []))
            ) for i, layer_size in enumerate(self.layers)
        ]
        self.activation_function = vectorize(
            lambda x: activation_function(x - activation_threshold)
        )

    def fill_layer(self, i, values):
        self.neurons[i][:self.layers[i]] = values

    def run_inputs(self, inputs):
        self.fill_layer(0, array(inputs))

        for i in range(len(self.layers) - 1):
            self.fill_layer(
                i + 1,
                self.activation_function(
                    self.neurons[i].dot(self.relations[i])
                )
            )

        return self.neurons[-1]

    def get_dimensions(self):
        return [
            (
                self.layers[i] + len(self.bias.get(i, [])),
                self.layers[i + 1]
            ) for i in range(len(self.layers) - 1)
        ]
