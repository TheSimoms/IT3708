from common.moea.reproduction_functions import splice_genome, genome_bit_mutation


class BaseProblem:
    def __init__(self, name):
        self.name = name

    @property
    def individual_class(self):
        raise NotImplementedError

    def generate_population(self, population_size, genome_size, **kwargs):
        raise NotImplementedError

    def fitness_function(self, genome, **kwargs):
        raise NotImplementedError

    def represent_genome(self, genome, **kwargs):
        raise NotImplementedError

    @staticmethod
    def crossover_function():
        return splice_genome

    @staticmethod
    def mutation_function(**kwargs):
        return genome_bit_mutation(**kwargs)

    @staticmethod
    def domination_function():
        raise NotImplementedError

    @staticmethod
    def extra_parameters():
        return {}
