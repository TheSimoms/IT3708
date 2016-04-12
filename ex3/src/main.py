from copy import deepcopy

from flatland import Flatland
from problem import Problem
from gui import GUI

from common.ann.ann import SimpleNeuralNetwork
from common.ann.utils import sigmoid_function
from common.ea.ea import EA
from common.ea.adult_selection_functions import mixing
from common.ea.parent_selection_functions import tournament_selection
from common.utils.parameters import get_boolean_parameter, get_numeric_parameter
from common.ea.analysis import plot_results

from constants import *


class FlatlandANN:
    def __init__(
            self, network_layers, dynamic_scenarios=False, number_of_bits=1,
            network_activation_function=sigmoid_function, network_activation_threshold=0.0,
            flatland_dimensions=(10, 10), flatland_distributions=(1/3, 1/3), flatland_number_of_steps=60,
            flatland_activation_threshold=0.5, number_of_scenarios=1
    ):
        self.dynamic_scenarios = dynamic_scenarios
        self.number_of_scenarios = number_of_scenarios

        self.network = SimpleNeuralNetwork(network_layers, network_activation_function, network_activation_threshold)
        self.flatland = Flatland(
            flatland_dimensions, flatland_distributions, flatland_number_of_steps, flatland_activation_threshold
        )

        self.problem = Problem(number_of_bits, self.network, self.flatland)

        genome_size = number_of_bits * sum(x * y for x, y in self.network.get_dimensions())
        number_of_generations = 50

        if self.dynamic_scenarios:
            self.scenarios = [
                [self.flatland.clone() for _ in range(self.number_of_scenarios)] for _ in range(number_of_generations)
            ]
        else:
            scenario_base = [self.flatland.clone() for _ in range(self.number_of_scenarios)]

            self.scenarios = [
                deepcopy(scenario_base) for _ in range(number_of_generations)
            ]

        self.ea = EA({
            'problem': self.problem,
            'genome_size': genome_size,
            'max_number_of_generations': number_of_generations,
            'adult_selection_function': mixing,
            'parent_selection_function': tournament_selection,
            'parameters': {
                'flatland_scenarios': self.scenarios,
                'group_size': 50,
                'epsilon': 0.1
            }
        })

    def run_scenario(self, i, scenario):
        scenario_copy = deepcopy(scenario)

        print('\nScenario: %d' % (i + 1))

        moves = scenario_copy.run(self.network)

        print('Results:')
        print('\tFood eaten: %s/%s' % (scenario_copy.agent.eaten_food_count, scenario.get_value_count(FOOD)))
        print('\tPoison eaten: %s/%s' % (scenario_copy.agent.eaten_poison_count, scenario.get_value_count(POISON)))

        GUI(self.problem.name, scenario, moves)

    def run(self):
        print('')

        results = self.ea.run()

        if get_boolean_parameter('\nDo you want to see results from EA run'):
            plot_results(results)

        print('\nReady to run the agent!')

        if self.dynamic_scenarios:
            scenarios = [self.flatland.clone() for _ in range(self.number_of_scenarios)]
        else:
            if get_boolean_parameter('Simulate using random scenario%s' % (
                    '' if self.number_of_scenarios == 1 else 's')
            ):
                scenarios = [self.flatland.clone() for _ in range(self.number_of_scenarios)]
            else:
                scenarios = [deepcopy(scenario) for scenario in self.scenarios[-1]]

        self.network.relations = results['best_individual'].phenotype

        for i, scenario in enumerate(scenarios):
            self.run_scenario(i, scenario)


if __name__ == '__main__':
    FlatlandANN(
        [6, 3],
        dynamic_scenarios=get_boolean_parameter('Dynamic scenarios'),
        number_of_scenarios=get_numeric_parameter('Number of scenarios', int)
    ).run()
