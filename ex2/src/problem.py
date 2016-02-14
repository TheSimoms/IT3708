class Problem:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def generate_population(population_size, genome_size, **kwargs):
        raise NotImplemented

    @staticmethod
    def fitness_function(phenotype, **kwargs):
        raise NotImplemented

    @staticmethod
    def genome_to_phenotype(genome, **kwargs):
        raise NotImplemented

    @staticmethod
    def represent_phenotype(phenotype, **kwargs):
        raise NotImplemented

    @staticmethod
    def crossover_function():
        raise NotImplemented

    @staticmethod
    def mutation_function():
        raise NotImplemented
