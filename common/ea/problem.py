from common.ea.reproduction_functions import mix_genome, genome_bit_mutation
from common.ea.utils import random_bits


class BaseProblem:
    def __init__(self, name, **kwargs):
        self.name = name

    @staticmethod
    def generate_population(population_size, genome_size, **kwargs):
        return [random_bits(genome_size) for _ in range(population_size)]

    def fitness_function(self, phenotype, **kwargs):
        raise NotImplemented

    def genome_to_phenotype(self, genome, **kwargs):
        raise NotImplemented

    def represent_phenotype(self, phenotype, **kwargs):
        raise NotImplemented

    @staticmethod
    def crossover_function():
        return mix_genome

    @staticmethod
    def mutation_function(**kwargs):
        return genome_bit_mutation(**kwargs)

    @staticmethod
    def extra_parameters():
        return {}
