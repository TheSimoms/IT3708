from utils import generate_string_population
from problem import Problem
from reproduction_functions import splice_genome, genome_string_mutation
from parameters import get_numeric_parameter, get_boolean_parameter


class SurprisingSequences(Problem):
    def __init__(self):
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

        sequences = set()
        err = 0

        for i in range(length - 1):
            for j in range(i + 1, length):
                sequence = '%s%s%s' % (phenotype[i], j - i - 1, phenotype[j])

                if sequence in sequences:
                    err += 1

                    if kwargs.get('L') is not None:
                        return float(j) / kwargs.get('L')
                else:
                    sequences.add(sequence)

                if kwargs.get('isLocal'):
                    break

        return 1.0 / (1.0 + err)

    @staticmethod
    def genome_to_phenotype(genome, **kwargs):
        return tuple(genome)

    def represent_phenotype(self, phenotype, **kwargs):
        return 'S=%d, L=%d, %s' % (
            kwargs.get('S'), len(phenotype) if kwargs.get('L') is None else kwargs.get('L'), ', '.join(phenotype))

    @staticmethod
    def crossover_function():
        return splice_genome

    @staticmethod
    def mutation_function():
        return genome_string_mutation

    @staticmethod
    def extra_parameters():
        return {
            'S': get_numeric_parameter('S', int),
            'L': get_numeric_parameter('L', int),
            'isLocal': get_boolean_parameter('Locally surprising')
        }
