from utils import generate_bit_population, bit_string_to_ints
from problem import Problem
from reproduction_functions import mix_genome, genome_bit_mutation


class OneMax(Problem):
    def __init__(self):
        super().__init__('One-Max')

        self.target_phenotype = None

    @staticmethod
    def generate_population(population_size, genome_size, **kwargs):
        return generate_bit_population(population_size=population_size, genome_size=genome_size)

    def fitness_function(self, phenotype, **kwargs):
        if self.target_phenotype is not None:
            score = 0.0

            for i in range(len(phenotype)):
                if self.target_phenotype[i] == phenotype:
                    score += 1

            return score / len(phenotype)

        return phenotype.count(1) / len(phenotype)

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
