from common.ea.utils import crossover

from common.moea.parent_selection_functions import tournament_selection


class Population:
    def __init__(self):
        self.population = []
        self.fronts = []

    def extend(self, individuals):
        self.population.extend(individuals)


class MOEA:
    def __init__(self, parameters, log=True):
        self.population_size = parameters.get('population_size', 200)
        self.genome_size = parameters.get('genome_size')

        self.problem = parameters.get('problem')

        self.parameters = parameters.get('parameters', {
            'group_size': 10,
            'epsilon': 0.5
        })

        self.crossover_probability = parameters.get('crossover_probability', 0.9)
        self.mutation_probability = parameters.get('mutation_probability', 0.9)

        self.parent_selection_function = tournament_selection

        self.max_number_of_generations = parameters.get('max_number_of_generations', 100)
        self.target_fitness = parameters.get('target_fitness', None)

        self.log = log

        self.population = Population()

    def __initialize(self):
        self.population.population = self.problem.generate_population(
            population_size=self.population_size, genome_size=self.genome_size, **self.parameters
        )

    def __generate_fitness_values(self, population):
        for individual in population:
            individual.fitness = self.problem.fitness_function(
                individual=individual, **self.parameters
            )

    def __generate_fronts(self, population=None):
        if population is None:
            population = self.population

        self.__generate_fitness_values(population.population)

        population.fronts.append([])

        for individual in population.population:
            individual.number_of_dominating_individuals = 0
            individual.dominated_individuals = set()

            for neighbour in population.population:
                if individual == neighbour:
                    continue

                if individual.dominates(neighbour):
                    individual.dominated_individuals.add(neighbour)
                elif neighbour.dominates(individual):
                    individual.number_of_dominating_individuals += 1

            if individual.number_of_dominating_individuals == 0:
                population.fronts[0].append(individual)

                individual.rank = 0

        i = 0

        while len(population.fronts[i]) > 0:
            temp_front = []

            for individual in population.fronts[i]:
                for dominated_individual in individual.dominated_individuals:
                    dominated_individual.number_of_dominating_individuals -= 1

                    if dominated_individual.number_of_dominating_individuals == 0:
                        dominated_individual.rank = i + 1

                        temp_front.append(dominated_individual)

            i += 1

            population.fronts.append(temp_front)

    def __calculate_crowding_distance(self, front):
        if len(front) > 0:
            number_of_individuals = len(front)

            for individual in front:
                individual.distance = 0

            for fitness_index in range(self.problem.number_of_fitness_values):
                front.sort(key=lambda x: x.fitness[fitness_index])

                front[0].distance = self.problem.maximum_fitness_values[fitness_index]
                front[number_of_individuals-1].distance = self.problem.maximum_fitness_values[fitness_index]

                for i, individual in enumerate(front[1: number_of_individuals-1]):
                    front[i].distance = \
                        (front[i+1].distance - front[i-1].distance) / \
                        (
                            self.problem.maximum_fitness_values[fitness_index] -
                            self.problem.minimum_fitness_values[fitness_index]
                        )

    def __calculate_crowding_distances(self):
        for front in self.population.fronts:
            self.__calculate_crowding_distance(front)

    def __generate_parents(self):
        return self.parent_selection_function(
            population=self.population.population, **self.parameters
        )

    def __mutation_function(self, genome):
        return self.problem.mutation_function(
            genome=genome, probability=self.mutation_probability, **self.parameters
        )

    def __generate_offspring(self):
        # Generate mating pairs
        mating_pairs = self.__generate_parents()

        # Add best individuals to the child pool (elitism)
        children = []

        for pair in mating_pairs:
            genomes = map(
                lambda genome: self.__mutation_function(genome),
                crossover(
                    pair,
                    self.crossover_probability,
                    self.problem.crossover_function()
                )
            )

            children.extend(self.problem.individual_class(genome) for genome in genomes)

        return children[:self.population_size]

    def __log(self):
        print('Generation number: %d' % (self.parameters['generation_number'] + 1))

    def run(self):
        self.parameters['generation_number'] = 0

        self.__initialize()

        self.__generate_fronts()
        self.__calculate_crowding_distances()

        old_population = None

        while True:
            try:
                self.population.extend(self.__generate_offspring())
                self.__generate_fronts()

                population = Population()

                i = 0

                while len(population.population) + len(self.population.fronts[i]) <= self.population_size:
                    self.__calculate_crowding_distance(self.population.fronts[i])

                    population.extend(self.population.fronts[i])

                    i += 1

                self.__calculate_crowding_distance(self.population.fronts[i])

                population.extend(
                    sorted(self.population.fronts[i])[:self.population_size-len(population.population)]
                )

                old_population = self.population
                self.population = population

                if self.log:
                    self.__log()

                if self.max_number_of_generations is not None and \
                        self.parameters['generation_number'] + 1 >= self.max_number_of_generations:
                    print('Maximum number of generations reached!')

                    break

                self.parameters['generation_number'] += 1

            except KeyboardInterrupt:
                break

        self.__generate_fronts(old_population)

        return {
            'generation_number': self.parameters['generation_number'],
            'population': old_population
        }
