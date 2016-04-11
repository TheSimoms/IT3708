from copy import deepcopy

from ann import ANN
from flatland import Flatland
from problem import Problem
from gui import GUI

from utils import sigmoid_function

from common.ea.ea import EA
from common.ea.adult_selection_functions import mixing
from common.utils.parameters import get_boolean_parameter, get_numeric_parameter


class FlatlandANN:
    def __init__(
            self, network_layers, network_bias, dynamic_scenarios=False, number_of_bits=1,
            network_activation_function=sigmoid_function, network_activation_threshold=0.0,
            flatland_dimensions=(10, 10), flatland_distributions=(1/3, 1/3), flatland_number_of_steps=60,
            flatland_activation_threshold=0.5, number_of_scenarios=1
    ):
        self.dynamic_scenarios = dynamic_scenarios

        self.network = ANN(network_layers, network_activation_function, network_activation_threshold, network_bias)
        self.flatland = Flatland(
            flatland_dimensions, flatland_distributions, flatland_number_of_steps, flatland_activation_threshold
        )

        self.problem = Problem(number_of_bits, self.network, self.flatland)

        genome_size = number_of_bits * sum(x * y for x, y in self.network.get_dimensions())
        number_of_generations = 30

        if self.dynamic_scenarios:
            scenarios = [
                [self.flatland.clone() for _ in range(number_of_scenarios)] for _ in range(number_of_generations)
            ]
        else:
            scenarios = [
                [deepcopy(self.flatland) for _ in range(number_of_scenarios)] for _ in range(number_of_generations)
            ]

        self.ea = EA({
            'problem': self.problem,
            'genome_size': genome_size,
            'max_number_of_generations': number_of_generations,
            'adult_selection_function': mixing,
            'parameters': {
                'flatland_scenarios': scenarios,
                'group_size': 50,
                'epsilon': 0.5
            }
        })

    def run(self):
        print('')

        best_individual = self.ea.run()['best_individual']

        print('\nReady to run the agent!')

        if self.dynamic_scenarios:
            flatland = self.flatland.clone()
        else:
            if get_boolean_parameter('Simulate using random scenario'):
                flatland = self.flatland.clone()
            else:
                flatland = deepcopy(self.flatland)

        self.network.relations = best_individual.phenotype

        moves = flatland.run(self.network)

        print('\nResults:')
        print('Food eaten: %s/%s' % (flatland.agent.eaten_food_count, flatland.agent.total_food_count))
        print('Poison eaten: %s/%s' % (flatland.agent.eaten_poison_count, flatland.agent.total_poison_count))

        GUI(self.problem.name, flatland, moves)


if __name__ == '__main__':
    FlatlandANN(
        [6, 3], {0: [1.0]},
        dynamic_scenarios=get_boolean_parameter('Dynamic scenarios'),
        number_of_scenarios=get_numeric_parameter('Number of scenarios', int)
    ).run()
