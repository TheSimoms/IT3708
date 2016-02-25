from ea import EA
from parameters import get_boolean_parameter, get_numeric_parameter, get_choice_parameter, get_choice_sub_parameter

from problems.one_max import OneMax
from problems.lolz import LOLZ
from problems.surprising_sequences import SurprisingSequences

from analysis import run_analysis_problem
from utils import make_plot

from adult_selection_functions import ADULT_SELECTION_FUNCTIONS
from parent_selection_functions import PARENT_SELECTION_FUNCTIONS


def get_parameters():
    parameters = {
        'parameters': {},

        'population_size': get_numeric_parameter('Population size', int),
        'genome_size': get_numeric_parameter('Genome size', int),

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
            ['One-Max', OneMax, None],
            ['LOLZ', LOLZ, None],
            ['Surprising sequences', SurprisingSequences, None],
        ]
    )[0]

    parameters['parameters'].update(problem.extra_parameters())
    parameters['problem'] = problem(**parameters)

    print('')

    return parameters


def plot_results(results):
    make_plot([
        (results['fitness_data']['best'], 'Best'),
        (results['fitness_data']['worst'], 'Worst'),
        (results['fitness_data']['average'], 'Average'),
        (results['fitness_data']['standard_deviation'], 'Standard deviation'),
    ], results['problem'].name, 'Generation number', 'Fitness')


def run_problem():
    parameters = get_parameters()
    ea = EA(parameters)

    plot_results(ea.run())


def main():
    analysis = get_boolean_parameter('Run analysis')

    if analysis:
        run_analysis_problem()
    else:
        run_problem()


if __name__ == '__main__':
    main()
