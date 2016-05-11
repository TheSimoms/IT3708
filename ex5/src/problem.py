from numpy.random import permutation

from common.moea.problem import BaseProblem
from common.moea.individual import Individual
from common.moea.utils import genome_swap_mutation


class Problem(BaseProblem):
    def __init__(self, distances, costs):
        super().__init__('Multi-objective travelling salesman', 2)

        self.distances = distances
        self.costs = costs

    @property
    def individual_class(self):
        return Individual

    def generate_population(self, population_size, genome_size, **kwargs):
        return [self.individual_class(permutation(range(genome_size)).tolist()) for _ in range(population_size)]

    @staticmethod
    def __get_travel_values(individual, data):
        genome = individual.genome
        values = []

        for i in range(len(genome)):
            current_index = genome[i]

            if i == len(genome) - 1:
                next_index = genome[0]
            else:
                next_index = genome[i+1]

            if current_index > next_index:
                value = data[current_index][next_index]
            else:
                value = data[next_index][current_index]

            values.append(value)

        return values

    def __distance_fitness(self, individual):
        return sum(self.__get_travel_values(individual, self.distances))

    def __cost_fitness(self, individual):
        return sum(self.__get_travel_values(individual, self.costs))

    def fitness_function(self, individual, **kwargs):
        fitness = [
            self.__distance_fitness(individual),
            self.__cost_fitness(individual),
        ]

        for i in range(self.number_of_fitness_values):
            if self.minimum_fitness_values[i] is None or fitness[i] < self.minimum_fitness_values[i]:
                self.minimum_fitness_values[i] = fitness[i]
            if self.maximum_fitness_values[i] is None or fitness[i] > self.maximum_fitness_values[i]:
                self.maximum_fitness_values[i] = fitness[i]

        return fitness

    def represent_genome(self, genome, **kwargs):
        return str(genome)

    @staticmethod
    def mutation_function(**kwargs):
        return genome_swap_mutation(**kwargs)
