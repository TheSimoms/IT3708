import matplotlib.pyplot as plt

from ea import EA
from parameters import get_boolean_parameter, get_numeric_parameter, get_choice_parameter, get_choice_sub_parameter

from problems.one_max import OneMax
from problems.lolz import LOLZ
from problems.surprising_sequences import SurprisingSequences

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


def make_plot(data, title, x_axis_name, y_axis_name):
    plot = plt.subplot(111)

    for i in range(len(data)):
        plot.plot(range(len(data[i])), data[i], label='Run: %d' % (i+1))

    plt.title(title)

    plt.xlabel(x_axis_name)
    plt.ylabel(y_axis_name)

    box = plot.get_position()
    plot.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    plot.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.show()


def plot_results(results):
    make_plot([
        results['fitness_data']['best'],
        results['fitness_data']['worst'],
        results['fitness_data']['average'],
        results['fitness_data']['standard_deviation'],
    ], results['problem'].name, 'Generation_number', 'Fitness')


def plot_analysis_results(results, problem_name):
    make_plot(results, problem_name, 'Generation number', 'Max fitness')


def run_problem():
    parameters = get_parameters()
    ea = EA(parameters)

    plot_results(ea.run())


def run_one_max_analysis(problem, parameters):
    plot_analysis_results(
        [results['fitness_data']['best'] for results in run_analysis(10, parameters)], problem.name
    )


def run_lolz_analysis(problem, parameters):
    parameters['max_number_of_generations'] = 100
    parameters['parameters'].update({
        'z': 21
    })

    plot_analysis_results(
        [results['fitness_data']['best'] for results in run_analysis(10, parameters)], problem.name
    )


def run_surprising_sequences_analysis(problem, parameters):
    parameters['max_number_of_generations'] = 1000
    parameters['population_size'] = 200

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

        'population_size': 75,
        'genome_size': 40,

        'crossover_probability': 0.7,
        'mutation_probability': 0.9,

        'max_number_of_generations': 100,
        'target_fitness': 1.0,

        'adult_selection_function': ADULT_SELECTION_FUNCTIONS[0][1],
        'parent_selection_function': PARENT_SELECTION_FUNCTIONS[2][1]
    }

    problem_name, problem = get_choice_parameter(
        'Problem', [
            ['One-Max', 'one-max', OneMax],
            ['LOLZ', 'lolz', LOLZ],
            ['Surprising sequences', 'surprising_sequences', SurprisingSequences],
        ]
    )

    parameters['parameters'].update(problem.extra_parameters())

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


def main():
    analysis = get_boolean_parameter('Run analysis')

    if analysis:
        run_analysis_problem()
    else:
        run_problem()


if __name__ == '__main__':
    main()
