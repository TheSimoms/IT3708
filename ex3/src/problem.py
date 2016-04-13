from copy import deepcopy

from common.ea.problem import BaseProblem
from common.utils.utils import normalize_bitstring, fill_matrix


class Problem(BaseProblem):
    def __init__(self, number_of_bits, network, flatland):
        super().__init__('Flatland')

        self.number_of_bits = number_of_bits

        self.network = network
        self.flatland = flatland

    def fitness_function(self, phenotype, **kwargs):
        flatland_scenarios = kwargs.get('flatland_scenarios')[kwargs.get('generation_number')]

        self.network.relations = phenotype

        score = []

        for flatland in deepcopy(flatland_scenarios):
            flatland.run(self.network)

            score.append(flatland.agent.score)

        return sum(score) / len(score)

    def genome_to_phenotype(self, genome, **kwargs):
        return fill_matrix(
            [
                normalize_bitstring(genome[i:i + self.number_of_bits])
                for i in range(0, len(genome), self.number_of_bits)
            ],
            self.network.get_dimensions()
        )[0]

    def represent_phenotype(self, phenotype, **kwargs):
        return str(list(phenotype))
