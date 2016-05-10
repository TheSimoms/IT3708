from ex4.src.world import World
from ex4.src.problem import Problem
from ex4.src.gui import GUI
from ex4.src.agent import Agent, AgentWithWalls

from common.ann.crtnn import ContinuousTimeRecurrentNeuralNetwork, NormalNeuron, BiasNeuron

from common.ea.ea import EA
from common.ea.adult_selection_functions import mixing
from common.ea.parent_selection_functions import tournament_selection
from common.ea.analysis import plot_results

from common.utils.parameters import get_boolean_parameter


class BeerTracker:
    def __init__(self, has_walls=False, allow_drop=False, number_of_bits=8, world_dimensions=(30, 15)):
        if has_walls:
            self.agent_class = AgentWithWalls

            network_layers = (
                (
                    NormalNeuron(), NormalNeuron(), NormalNeuron(), NormalNeuron(),
                    NormalNeuron(), NormalNeuron(), NormalNeuron()
                ),
                (NormalNeuron(), NormalNeuron(), NormalNeuron(), NormalNeuron(), BiasNeuron(1.0)),
                (NormalNeuron(), NormalNeuron())
            )
        else:
            self.agent_class = Agent

            if allow_drop:
                network_layers = (
                    (NormalNeuron(), NormalNeuron(), NormalNeuron(), NormalNeuron(), NormalNeuron(), BiasNeuron(1.0)),
                    (NormalNeuron(), NormalNeuron(), BiasNeuron(1.0)),
                    (NormalNeuron(), NormalNeuron(), NormalNeuron())
                )
            else:
                network_layers = (
                    (NormalNeuron(), NormalNeuron(), NormalNeuron(), NormalNeuron(), NormalNeuron(), BiasNeuron(1.0)),
                    (NormalNeuron(), NormalNeuron(), BiasNeuron(1.0)),
                    (NormalNeuron(), NormalNeuron())
                )

        self.network = ContinuousTimeRecurrentNeuralNetwork(network_layers)
        self.world = World(world_dimensions)

        self.problem = Problem(number_of_bits, self.agent_class, self.world, self.network)

        self.ea = EA({
            'problem': self.problem,
            'genome_size': self.problem.genotype_size,
            'population_size': 400,
            'max_number_of_generations': 10,
            'adult_selection_function': mixing,
            'parent_selection_function': tournament_selection,
            'target_fitness': None,
            'parameters': {
                'group_size': 50,
                'epsilon': 0.3
            }
        })

    def run(self):
        print('')

        results = self.ea.run()

        if get_boolean_parameter('\nDo you want to see results from EA run'):
            plot_results(results)

        print('\nReady to run the agent!')

        self.network.apply_phenotype(results['best_individual'].phenotype)

        agent = self.agent_class(self.world, self.network)

        GUI(self.problem.name, agent)

        agent.run()

        print('\nCaught %s/%s small' % (agent.points[0], agent.points[0] + agent.points[3]))
        print('Avoided %s/%s large' % (agent.points[1], agent.points[1] + agent.points[2]))

        input('\nComplete! Press enter to exit.')


if __name__ == '__main__':
    _has_walls = get_boolean_parameter('Use walls')

    if not _has_walls:
        _allow_drop = get_boolean_parameter('Allow pull')
    else:
        _allow_drop = False

    BeerTracker(_has_walls, _allow_drop).run()
