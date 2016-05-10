class Individual:
    def __init__(self, genome):
        self.genome = genome
        self.fitness = []

        self.rank = None
        self.distance = None

        self.number_of_dominating_individuals = None
        self.dominated_individuals = set()

    def __lt__(self, individual):
        if (self.rank < individual.rank) or (
            (self.rank == individual.rank) and (self.distance < individual.distance)
        ):
            return 1
        else:
            return -1

    def set_fitness(self, fitness):
        self.fitness = fitness

    def dominates(self, individual):
        if self.fitness is None:
            raise Exception('ERROR')

        worse = True
        better = False

        for i in range(len(self.fitness)):
            worse = worse and self.fitness[i] > individual.fitness[i]
            better = better or self.fitness[i] < individual.fitness[i]

        return (not worse) and better
