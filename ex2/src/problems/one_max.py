from utils import generate_bit_population, generate_bit_individual, bit_string_to_ints, list_to_string
from problem import Problem
from parameters import get_boolean_parameter
from reproduction_functions import mix_genome, genome_bit_mutation


class OneMax(Problem):
    def __init__(self, **kwargs):
        super().__init__('One-Max')

        self.target_phenotype = [1] * kwargs['genome_size']

    @staticmethod
    def generate_population(population_size, genome_size, **kwargs):
        return generate_bit_population(population_size=population_size, genome_size=genome_size)

    def fitness_function(self, phenotype, **kwargs):
        phenotype_size = len(phenotype)

        return sum(self.target_phenotype[i] == phenotype[i] for i in range(phenotype_size)) / phenotype_size

    @staticmethod
    def genome_to_phenotype(genome, **kwargs):
        return bit_string_to_ints(genome)

    def represent_phenotype(self, phenotype, **kwargs):
        return list_to_string(phenotype)

    @staticmethod
    def crossover_function():
        return mix_genome

    @staticmethod
    def mutation_function(**kwargs):
        return genome_bit_mutation(**kwargs)
