from numpy.random import permutation

from common.moea.problem import BaseProblem
from common.moea.reproduction_functions import splice_genome, genome_bit_mutation

from ex5.src.individual import Individual


class Problem(BaseProblem):
    def __init__(self, costs, distances):
        super().__init__('Multi-objective travelling salesman')

        self.costs = costs
        self.distances = distances

    @property
    def individual_class(self):
        return Individual

    def generate_population(self, population_size, genome_size, **kwargs):
        return [self.individual_class(permutation(range(genome_size))) for _ in range(population_size)]

    def fitness_function(self, genome, **kwargs):
        raise NotImplementedError

    def represent_genome(self, genome, **kwargs):
        return str(genome)

    @staticmethod
    def crossover_function():
        return splice_genome

    @staticmethod
    def mutation_function(**kwargs):
        return genome_bit_mutation(**kwargs)

    @staticmethod
    def domination_function():
        raise NotImplementedError
