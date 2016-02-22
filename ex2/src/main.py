import matplotlib.pyplot as plt

from ea import EA
from parameters import get_boolean_parameter, get_numeric_parameter, get_choice_parameter, get_choice_sub_parameter

from problems.one_max import OneMax
from problems.lolz import LOLZ
from problems.surprising_sequences import SurprisingSequences

from utils import generate_bit_individual

from adult_selection_functions import ADULT_SELECTION_FUNCTIONS
from parent_selection_functions import PARENT_SELECTION_FUNCTIONS


def get_parameters():
    parameters = {
        'parameters': {},

        'population_size': get_numeric_parameter('Population size', int),
        'genome_size': get_numeric_parameter('Genome size', int),

        'number_of_children': get_numeric_parameter('Number of children from mating', int),

        'crossover_probability': get_numeric_parameter('Crossover probability', float),
        'mutation_probability': get_numeric_parameter('Mutation probability', float),

        'max_number_of_generations': get_numeric_parameter('Maximum number of generations', int, True),
        'target_fitness': 1.0,
    }

    adult_selection_function, adult_selection_function_parameters = get_choice_parameter(
        'Adult selection', ADULT_SELECTION_FUNCTIONS
    )

    parameters['adult_selection_function'] = adult_selection_function

    if adult_selection_function_parameters is not None:
        parameters['parameters'].update(get_choice_sub_parameter(adult_selection_function_parameters))

    parent_selection_function, parent_selection_function_parameters = get_choice_parameter(
        'Parent selection', PARENT_SELECTION_FUNCTIONS
    )

    parameters['parent_selection_function'] = parent_selection_function

    if parent_selection_function_parameters is not None:
        parameters['parameters'].update(get_choice_sub_parameter(parent_selection_function_parameters))

    problem = get_choice_parameter(
        'Problem', [
            ['One-Max', OneMax(), None],
            ['LOLZ', LOLZ(), None],
            ['Surprising sequences', SurprisingSequences(), None],
        ]
    )[0]

    parameters['problem'] = problem
    parameters['parameters'].update(problem.extra_parameters())

    print('')

    return parameters


def plot_results(results):
    plt.plot(results['fitness_data']['best'])
    plt.plot(results['fitness_data']['worst'])
    plt.plot(results['fitness_data']['average'])
    plt.plot(results['fitness_data']['standard_deviation'])

    plt.xlabel('Generation number')
    plt.ylabel('Fitness')

    plt.legend(['Best', 'Worst', 'Average', 'Standard deviation'], loc='lower right')
    plt.title(results['problem'].name)

    plt.show()


def plot_analysis_results(results, problem_name):
    for run in results:
        plt.plot(run)

    plt.xlabel('Generation number')
    plt.ylabel('Best fitness')

    plt.legend(['Run %d' % (i+1) for i in range(len(results))], loc='lower right')
    plt.title('Analysis')

    plt.show(problem_name)


def run_problem():
    parameters = get_parameters()
    ea = EA(parameters)

    plot_results(ea.run())


def run_analysis_problem():
    problem_name = get_choice_parameter(
        'Problem', [
            ['One-Max', 'one-max', None],
            ['LOLZ', 'lolz', None],
            ['Surprising sequences', 'surprising_sequences', None],
        ]
    )[0]

    if problem_name == 'one-max':
        problem = OneMax()
    elif problem_name == 'lolz':
        problem = LOLZ()
    else:
        problem = SurprisingSequences()

    parameters = {
        'problem': problem,
        'parameters': {
            'group_size': 25,
            'epsilon': 0.1
        },

        'population_size': 75,
        'genome_size': 40,

        'number_of_children': 2,

        'crossover_probability': 0.3,
        'mutation_probability': 0.9,

        'max_number_of_generations': 100,
        'target_fitness': 1.0,

        'adult_selection_function': ADULT_SELECTION_FUNCTIONS[0][1],
        'parent_selection_function': PARENT_SELECTION_FUNCTIONS[2][1]
    }

    if problem_name == 'one-max':
        if get_boolean_parameter('Random vector'):
            problem.target_phenotype = problem.genome_to_phenotype(generate_bit_individual(parameters['genome_size']))

        number_of_runs = 10
    elif problem_name == 'lolz':
        parameters['max_number_of_generations'] = 100
        parameters['parameters'].update({
            'z': 21
        })
        number_of_runs = 10
    else:
        number_of_runs = 10

    fitness_results = []

    for i in range(number_of_runs):
        try:
            print('Run: %d' % i)

            run_results = EA(parameters, log=False).run()

            fitness_results.append(run_results['fitness_data']['best'])

        except KeyboardInterrupt:
            break

    plot_analysis_results(fitness_results, problem.name)


def run_analysis():
    run_analysis_problem()


def main():
    analysis = get_boolean_parameter('Run analysis')

    if analysis:
        run_analysis()
    else:
        run_problem()


if __name__ == '__main__':
    main()
