from math import sqrt

from .utils import get_fitness, crossover


class Individual:
    def __init__(self, genome):
        self.genome = genome
        self.phenotype = None
        self.fitness = None


class EA:
    def __init__(self, parameters):
        self.problem = parameters.get('problem')
        self.parameters = parameters.get('parameters')

        self.population_size = parameters.get('population_size')
        self.genome_size = parameters.get('genome_size')

        self.number_of_generations = parameters.get('number_of_generations')

        self.crossover_probability = parameters.get('crossover_probability')
        self.mutation_probability = parameters.get('mutation_probability')

        self.adult_selection_function = parameters.get('adult_selection_function')
        self.parent_selection_function = parameters.get('parent_selection_function')

        self.crossover_function = parameters.get('crossover_function')
        self.mutation_function = parameters.get('mutation_function')

        self.max_number_of_generations = parameters.get('max_number_of_generations')
        self.target_fitness = parameters.get('target_fitness')

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
        return self.mutation_function(
            genome=genome, probability=self.mutation_probability, **self.parameters
        )

    def __generate_offspring(self, population):
        mating_pairs = self.__generate_parents(population)
        children = []

        for pair in mating_pairs:
            genomes = map(
                self.mutation_function,
                crossover(
                    pair,
                    self.crossover_probability,
                    self.crossover_function,
                    self.parameters['number_of_children']
                )
            )

            children.extend(Individual(genome) for genome in genomes)

        return children

    def __update_logging_data(self, population, best_individual, fitness_data, best_phenotypes):
        fitness = [get_fitness(individual) for individual in population]
        average_fitness = sum(fitness) / self.population_size

        fitness_data['best'].append(max(fitness))
        fitness_data['worst'].append(min(fitness))
        fitness_data['average'].append(average_fitness)
        fitness_data['standard_deviation'].append(
            sqrt(
                sum(
                    (get_fitness(individual) - average_fitness) ** 2 for individual in population
                ) / self.population_size
            )
        )

        best_phenotypes.append(best_individual.phenotype)

    def __log(self, generation_number, fitness_data, best_phenotypes):
        pass

    def __is_simulation_finished(self, generation_number, best_fitness):
        if generation_number >= self.max_number_of_generations:
            pass
        elif best_fitness >= self.target_fitness:
            pass
        else:
            return False

        return True

    def run(self):
        generation_number = 0

        fitness_data = {
            'best': [],
            'worst': [],
            'average': [],
            'standard_deviation': []
        }
        best_phenotypes = []

        population = []
        children = self.__initialize()

        while True:
            self.__generate_phenotypes(children)
            self.__generate_fitness_values(children)

            population = self.__generate_adult_population(population, children)
            children = self.__generate_offspring(population)
            best_individual = max(population, key=get_fitness)

            self.__update_logging_data(population, best_individual, fitness_data, best_phenotypes)
            self.__log(generation_number, fitness_data, best_phenotypes)

            if self.__is_simulation_finished(generation_number, best_individual.fitness):
                return {
                    'generation_number': generation_number,
                    'population': population,
                    'best_individual': best_individual,
                    'fitness_data': fitness_data,
                    'best_phenotypes': best_phenotypes
                }

            generation_number += 1
