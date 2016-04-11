from math import sqrt

from common.ea.utils import crossover
from common.ea.adult_selection_functions import full_selection
from common.ea.parent_selection_functions import fitness_proportionate


class Individual:
    def __init__(self, genome):
        self.genome = genome
        self.phenotype = None
        self.fitness = None


class EA:
    def __init__(self, parameters, log=True):
        self.problem = parameters.get('problem')
        self.parameters = parameters.get('parameters', {
            'group_size': 10,
            'epsilon': 0.5
        })

        self.population_size = parameters.get('population_size', 200)
        self.genome_size = parameters.get('genome_size')

        self.crossover_probability = parameters.get('crossover_probability', 0.9)
        self.mutation_probability = parameters.get('mutation_probability', 0.9)

        self.adult_selection_function = parameters.get('adult_selection_function', full_selection)
        self.parent_selection_function = parameters.get('parent_selection_function', fitness_proportionate)

        self.max_number_of_generations = parameters.get('max_number_of_generations', 100)
        self.target_fitness = parameters.get('target_fitness', 1)

        self.elitism_number = parameters.get('elitism_number', 5)

        self.log = log

    def __initialize(self):
        return [
            Individual(genome) for genome in self.problem.generate_population(
                population_size=self.population_size, genome_size=self.genome_size, **self.parameters
            )
        ]

    def __generate_phenotypes(self, individuals):
        for individual in individuals:
            individual.phenotype = self.problem.genome_to_phenotype(
                genome=individual.genome, **self.parameters
            )

    def __generate_fitness_values(self, individuals):
        for individual in individuals:
            individual.fitness = self.problem.fitness_function(
                phenotype=individual.phenotype, **self.parameters
            )

    def __generate_adult_population(self, old_population, children):
        return self.adult_selection_function(
            old_population=old_population, children=children, population_size=self.population_size, **self.parameters
        )

    def __generate_parents(self, population):
        return self.parent_selection_function(
            population=population, **self.parameters
        )

    def __mutation_function(self, genome):
        return self.problem.mutation_function(
            genome=genome, probability=self.mutation_probability, **self.parameters
        )

    def __generate_offspring(self, population):
        # Generate mating pairs
        mating_pairs = self.__generate_parents(population)

        # Add best individuals to the child pool (elitism)
        children = sorted(population, key=lambda individual: individual.fitness, reverse=True)[:self.elitism_number]

        for pair in mating_pairs:
            genomes = map(
                lambda genome: self.__mutation_function(genome),
                crossover(
                    pair,
                    self.crossover_probability,
                    self.problem.crossover_function()
                )
            )

            children.extend(Individual(genome) for genome in genomes)

        return children[:self.population_size]

    def __update_logging_data(self, population, best_individual, fitness_data, best_phenotypes):
        fitness = [individual.fitness for individual in population]
        average_fitness = sum(fitness) / self.population_size

        fitness_data['best'].append(max(fitness))
        fitness_data['worst'].append(min(fitness))
        fitness_data['average'].append(average_fitness)
        fitness_data['standard_deviation'].append(
            sqrt(
                sum(
                    (individual.fitness - average_fitness) ** 2 for individual in population
                ) / self.population_size
            )
        )

        best_phenotypes.append(best_individual.phenotype)

    def __log(self, fitness_data, best_phenotypes):
        print('Generation number: %d' % (self.parameters['generation_number'] + 1))

        print('Fitness:')
        print('\tBest: %.2f' % fitness_data['best'][-1])
        print('\tWorst: %.2f' % fitness_data['worst'][-1])
        print('\tAverage: %.2f' % fitness_data['average'][-1])
        print('\tStandard deviation: %.2f' % fitness_data['standard_deviation'][-1])

        print('Best phenotype: %s\n' % self.problem.represent_phenotype(
            phenotype=best_phenotypes[-1], **self.parameters
        ))

    def __is_simulation_finished(self, best_fitness):
        if self.max_number_of_generations is not None and \
                        self.parameters['generation_number'] + 1 >= self.max_number_of_generations:
            print('Maximum number of generations reached!')
        elif self.target_fitness is not None and best_fitness >= self.target_fitness:
            print('Target fitness reached!')
        else:
            return False

        return True

    def run(self):
        self.parameters['generation_number'] = 0

        fitness_data = {
            'best': [],
            'worst': [],
            'average': [],
            'standard_deviation': []
        }
        best_phenotypes = []

        population = []
        children = self.__initialize()

        best_individual = None
        best_run_individual = None

        while True:
            try:
                self.__generate_phenotypes(children)
                self.__generate_fitness_values(children)

                population = self.__generate_adult_population(population, children)

                best_individual = max(population, key=lambda individual: individual.fitness)
                best_run_individual = max(
                    (best_individual, best_run_individual), key=lambda individual: individual.fitness
                ) if best_run_individual is not None else best_individual

                children = self.__generate_offspring(population)

                self.__update_logging_data(population, best_individual, fitness_data, best_phenotypes)

                if self.log:
                    self.__log(fitness_data, best_phenotypes)

                if self.__is_simulation_finished(best_individual.fitness):
                    break

                self.parameters['generation_number'] += 1
            except KeyboardInterrupt:
                break

        return {
            'generation_number': self.parameters['generation_number'],
            'population': population,
            'best_individual': best_individual,
            'best_run_individual': best_run_individual,
            'fitness_data': fitness_data,
            'best_phenotypes': best_phenotypes,
            'problem': self.problem
        }
