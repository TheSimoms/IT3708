class Problem:
    def __init__(self, name, **kwargs):
        self.name = name

    @staticmethod
    def generate_population(population_size, genome_size, **kwargs):
        raise NotImplemented

    def fitness_function(self, phenotype, **kwargs):
        raise NotImplemented

    @staticmethod
    def genome_to_phenotype(genome, **kwargs):
        raise NotImplemented

    def represent_phenotype(self, phenotype, **kwargs):
        raise NotImplemented

    @staticmethod
    def crossover_function():
        raise NotImplemented

    @staticmethod
    def mutation_function():
        raise NotImplemented

    @staticmethod
    def extra_parameters():
        return {}
