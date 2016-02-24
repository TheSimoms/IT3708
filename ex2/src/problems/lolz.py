from utils import generate_bit_population, bit_string_to_ints, list_to_string
from problem import Problem
from reproduction_functions import mix_genome, genome_bit_mutation
from parameters import get_numeric_parameter


class LOLZ(Problem):
    def __init__(self, **kwargs):
        super().__init__('LOLZ')

    @staticmethod
    def generate_population(population_size, genome_size, **kwargs):
        return generate_bit_population(population_size=population_size, genome_size=genome_size)

    def fitness_function(self, phenotype, **kwargs):
        score = 0
        leading_character = phenotype[0]

        phenotype_size = len(phenotype)

        for bit in phenotype:
            if bit != leading_character:
                break

            score += 1

        if leading_character == 0:
            score = min(kwargs.get('z'), score)

        return 1 - ((phenotype_size - score) / phenotype_size)

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

    @staticmethod
    def extra_parameters():
        return {
            'z': get_numeric_parameter('Z', int)
        }
