from copy import deepcopy

from common.ea.problem import BaseProblem
from common.utils.utils import normalize_bitstring, fill_matrix


class Problem(BaseProblem):
    def __init__(self, number_of_bits, agent_class, world, network, score_weights):
        super().__init__('Beer tracker')

        self.number_of_bits = number_of_bits

        self.agent_class = agent_class
        self.world = world
        self.network = network
        self.score_weights = score_weights

        phenotype_sizes = self.network.calculate_phenotype_size()

        self.genotype_size = self.number_of_bits * (
            2 * phenotype_sizes['neurons'] +
            sum(i * j for i, j in phenotype_sizes['looping_connections']) +
            sum(i * j for i, j in phenotype_sizes['intra_connections'])
        )

    """@staticmethod
    def generate_population(population_size, genome_size, **kwargs):
        population = []

        for i in range(population_size):
            weights = [[]]

        return [random_bits(genome_size) for _ in range(population_size)]"""

    def fitness_function(self, phenotype, **kwargs):
        world = deepcopy(self.world)
        network = deepcopy(self.network)

        network.apply_phenotype(phenotype)

        agent = self.agent_class(world, network, self.score_weights)
        agent.run()

        return agent.score

    def genome_to_phenotype(self, genome, **kwargs):
        values = [
            normalize_bitstring(
                genome[i:i + self.number_of_bits]
            ) for i in range(0, self.genotype_size, self.number_of_bits)
        ]

        phenotype_sizes = self.network.calculate_phenotype_size()

        phenotype = {
            'gains': list(map(lambda x: 1.0 + 4.0 * x, values[:phenotype_sizes['neurons']])),
            'time': list(map(lambda x: 1.0 + x, values[phenotype_sizes['neurons']:]))
        }

        phenotype['looping_connections'], values = fill_matrix(
            values, phenotype_sizes['looping_connections'], mapping_function=lambda x: 10.0 * x - 5.0
        )
        phenotype['intra_connections'], values = fill_matrix(
            values, phenotype_sizes['intra_connections'], mapping_function=lambda x: 10.0 * x - 5.0
        )

        return phenotype

    def represent_phenotype(self, phenotype, **kwargs):
        return str(phenotype)
