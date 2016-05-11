from common.moea.utils import ordered_crossover


class BaseProblem:
    def __init__(self, name, number_of_fitness_values):
        self.name = name
        self.number_of_fitness_values = number_of_fitness_values

        self.minimum_fitness_values = [None] * self.number_of_fitness_values
        self.maximum_fitness_values = [None] * self.number_of_fitness_values

    @property
    def individual_class(self):
        raise NotImplementedError

    def generate_population(self, population_size, genome_size, **kwargs):
        raise NotImplementedError

    def fitness_function(self, individual, **kwargs):
        raise NotImplementedError

    def represent_genome(self, genome, **kwargs):
        raise NotImplementedError

    @staticmethod
    def crossover_function():
        return ordered_crossover

    @staticmethod
    def mutation_function(**kwargs):
        raise NotImplementedError

    @staticmethod
    def extra_parameters():
        return {}
