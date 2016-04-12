from numpy import zeros, vectorize, array


class ANN:
    def __init__(self, layers, activation_function, activation_threshold=0.0):
        self.layers = layers

        self.relations = None
        self.neurons = [
            zeros(layer_size) for i, layer_size in enumerate(self.layers)
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
                self.layers[i],
                self.layers[i + 1]
            ) for i in range(len(self.layers) - 1)
        ]
