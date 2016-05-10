class BaseIndividual:
    def __init__(self, genome):
        self.genome = genome
        self.fitness = None

        self.rank = None
        self.distance = None
        self.dominated_individuals = set()

    def set_fitness(self, fitness):
        self.fitness = fitness

    def dominates(self, individual):
        raise NotImplementedError
