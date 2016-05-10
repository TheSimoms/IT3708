from common.moea.individual import BaseIndividual


class Individual(BaseIndividual):
    def __init__(self, genome):
        super().__init__(genome)

    def dominates(self, individual):
        raise NotImplementedError
