from utils import generate_bit_population, bit_string_to_ints
from problem import Problem
from reproduction_functions import mix_genome, genome_bit_mutation
from parameters import get_numeric_parameter


class LOLZ(Problem):
    def __init__(self):
        super().__init__('LOLZ')

    @staticmethod
    def generate_population(population_size, genome_size, **kwargs):
        return generate_bit_population(population_size=population_size, genome_size=genome_size)

    def fitness_function(self, phenotype, **kwargs):
        leading_character = phenotype[0]

        for i in range(1, len(phenotype)):
            if phenotype[i] != leading_character:
                score = i

                if leading_character == 0 and score > kwargs['z']:
                    score = kwargs['z']

                return score / len(phenotype)

        return 1.0

    @staticmethod
    def genome_to_phenotype(genome, **kwargs):
        return bit_string_to_ints(genome)

    @staticmethod
    def represent_phenotype(phenotype, **kwargs):
        return str(phenotype)

    @staticmethod
    def crossover_function():
        return mix_genome

    @staticmethod
    def mutation_function():
        return genome_bit_mutation

    @staticmethod
    def extra_parameters():
        return {
            'z': get_numeric_parameter('Z', int)
        }
