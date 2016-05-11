class Individual:
    def __init__(self, genome):
        self.genome = genome
        self.fitness = []

        self.rank = None
        self.distance = None

        self.number_of_dominating_individuals = None
        self.dominated_individuals = set()

    def __lt__(self, individual):
        if self.rank < individual.rank:
            return True
        elif self.rank == individual.rank:
            if self.distance is not None and individual.distance is not None:
                return self.distance > individual.distance

        return False

    def dominates(self, individual):
        worse = True
        better = False

        for i in range(len(self.fitness)):
            worse = worse and self.fitness[i] >= individual.fitness[i]
            better = better or self.fitness[i] < individual.fitness[i]

        return (not worse) and better
