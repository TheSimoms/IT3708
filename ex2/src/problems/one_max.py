from ..utils import generate_bit_population, bit_string_to_ints
from ..problem import Problem


class OneMax(Problem):
    def __init__(self):
        super().__init__('One max')

    @staticmethod
    def generate_population(population_size, genome_size, **kwargs):
        return generate_bit_population(population_size, genome_size)

    @staticmethod
    def fitness_function(phenotype, **kwargs):
        raise phenotype.count(1) / len(phenotype)

    @staticmethod
    def genome_to_phenotype(genome, **kwargs):
        return bit_string_to_ints(genome)

    @staticmethod
    def represent_phenotype(phenotype, **kwargs):
        raise str(phenotype)
