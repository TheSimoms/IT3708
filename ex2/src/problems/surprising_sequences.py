from common.ea.utils import generate_string_population
from common.ea.reproduction_functions import splice_genome, genome_string_mutation
from common.ea.problem import BaseProblem
from common.utils.parameters import get_numeric_parameter, get_boolean_parameter


class SurprisingSequences(BaseProblem):
    def __init__(self, **kwargs):
        super().__init__('Surprising sequences')

    @staticmethod
    def generate_population(population_size, genome_size, **kwargs):
        return generate_string_population(
            population_size=population_size,
            genome_size=genome_size,
            **kwargs
        )

    def fitness_function(self, phenotype, **kwargs):
        length = len(phenotype)
        sequences = []

        for i in range(length - 1):
            for j in range(i + 1, length):
                sequences.append('%s%s%s' % (phenotype[i], j - i - 1, phenotype[j]))

                if kwargs.get('isLocal'):
                    break

        return (len(set(sequences)) - 1) / (len(sequences) - 1)

    def genome_to_phenotype(self, genome, **kwargs):
        return tuple(genome)

    def represent_phenotype(self, phenotype, **kwargs):
        return 'S=%d, L=%d, %s' % (
            kwargs.get('S'), len(phenotype), ', '.join(phenotype))

    @staticmethod
    def crossover_function():
        return splice_genome

    @staticmethod
    def mutation_function(**kwargs):
        return genome_string_mutation(**kwargs)

    @staticmethod
    def extra_parameters():
        return {
            'S': get_numeric_parameter('S', int),
            'isLocal': get_boolean_parameter('Locally surprising')
        }
