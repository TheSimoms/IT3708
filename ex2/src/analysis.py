import copy

import numpy as np

from common.ea.ea import EA
from common.ea.utils import generate_bit_individual
from common.ea.analysis import plot_analysis_results
from common.ea.parent_selection_functions import PARENT_SELECTION_FUNCTIONS
from common.ea.adult_selection_functions import ADULT_SELECTION_FUNCTIONS
from common.utils.parameters import get_boolean_parameter, get_choice_parameter
from problems.one_max import OneMax
from problems.lolz import LOLZ
from problems.surprising_sequences import SurprisingSequences


def run_one_max_analysis(problem, parameters):
    variations = []

    number_of_runs = 10

    if get_boolean_parameter('Random target vector'):
        problem.target_phenotype = problem.genome_to_phenotype(generate_bit_individual(parameters['genome_size']))

        number_of_runs = 10

        variations.append((parameters, 'random_vector'))
    else:
        vary_rates = get_boolean_parameter('Vary rates')
        vary_parent_selection = get_boolean_parameter('Vary parent selection')

        if vary_rates:

            for crossover_probability in np.arange(0.1, 1.0, 0.1):
                for mutation_probability in np.arange(0.1, 1.0, 0.1):
                    variation = copy.deepcopy(parameters)

                    variation['parent_selection_function'] = PARENT_SELECTION_FUNCTIONS[0][1]

                    variation['crossover_probability'] = crossover_probability
                    variation['mutation_probability'] = mutation_probability

                    variations.append((variation, '%s, %s' % (str(crossover_probability), str(mutation_probability))))

        if vary_parent_selection:
            for selection_function_choices in PARENT_SELECTION_FUNCTIONS:
                variation = copy.deepcopy(parameters)

                function_name = selection_function_choices[0]
                function = selection_function_choices[1]

                if selection_function_choices[2] is not None:
                    for group_size in range(10, variation['population_size'] - 5, variation['population_size'] // 5):
                        for epsilon in np.arange(0.1, 1.0, 0.1):
                            variation = copy.deepcopy(parameters)

                            variation['parent_selection_function'] = function

                            variation['parameters']['group_size'] = group_size
                            variation['parameters']['epsilon'] = epsilon

                            variations.append(
                                (variation, '%s, %s, %s' % (function_name, str(group_size), str(epsilon))))
                else:
                    variation['parent_selection_function'] = function

                    variations.append((variation, function_name))

        if not (vary_rates or vary_parent_selection):
            variations.append((parameters, None))

    for variation, file_name in variations:
        plot_analysis_results([results['fitness_data']['best'] for results in run_analysis(
            number_of_runs, variation
        )], problem.name, file_name)


def run_lolz_analysis(problem, parameters):
    parameters['parameters'].update({
        'z': 21
    })

    plot_analysis_results(
        [results['fitness_data']['best'] for results in run_analysis(20, parameters)], problem.name, 'lolz'
    )


def run_surprising_sequences_analysis(problem, parameters):
    parameters['max_number_of_generations'] = 1000

    parameters['parameters']['isLocal'] = get_boolean_parameter('Local search')

    results = {}

    for S in [3, 5, 10, 15, 20]:
        parameters['parameters']['S'] = S
        results[S] = None

        print('\nS: %d' % S)

        L = S

        while True:
            print('L: %d' % L)

            parameters['genome_size'] = L

            success = False

            for run in range(15):
                print('Run: %d' % run)

                run_results = EA(parameters, log=False).run()

                if run_results['best_individual'].fitness >= 1.0:
                    results[S] = (
                        run_results['best_individual'], L, run_results['generation_number']
                    )

                    success = True

                    break

            if not success:
                break

            L += 1

    print('\nLocal search' if parameters['parameters']['isLocal'] else 'Global search')

    for S in sorted(results.keys()):
        if results[S] is not None:
            print('')
            print(problem.represent_phenotype(
                phenotype=results[S][0].phenotype, S=S, L=results[S][1]
            ))
            print('Population size: %d, number of generations: %d' % (parameters['population_size'], results[S][2]))


def run_analysis_problem():
    parameters = {
        'parameters': {
            'group_size': 50,
            'epsilon': 0.1
        },

        'population_size': 400,
        'genome_size': 40,

        'crossover_probability': 0.9,
        'mutation_probability': 0.9,

        'max_number_of_generations': 100,
        'target_fitness': 1.0,

        'adult_selection_function': ADULT_SELECTION_FUNCTIONS[0][1],
        'parent_selection_function': PARENT_SELECTION_FUNCTIONS[2][1],

        'elitism_number': 0
    }

    problem_name, problem = get_choice_parameter(
        'Problem', [
            ['One-Max', 'one-max', OneMax],
            ['LOLZ', 'lolz', LOLZ],
            ['Surprising sequences', 'surprising_sequences', SurprisingSequences],
        ]
    )

    problem = problem(**parameters)

    parameters['problem'] = problem

    if problem_name == 'one-max':
        run_one_max_analysis(problem, parameters)
    elif problem_name == 'lolz':
        run_lolz_analysis(problem, parameters)
    elif problem_name == 'surprising_sequences':
        run_surprising_sequences_analysis(problem, parameters)


def run_analysis(number_of_runs, parameters):
    fitness_results = []

    for i in range(number_of_runs):
        try:
            print('Run: %d' % i)

            run_results = EA(parameters, log=False).run()

            fitness_results.append(run_results)

        except KeyboardInterrupt:
            break

    return fitness_results
