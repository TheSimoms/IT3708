from common.moea.moea import MOEA

from common.utils.parameters import get_numeric_parameter, get_boolean_parameter

from ex5.src.loader import load_data
from ex5.src.problem import Problem
from ex5.src.analysis import plot_single_run, plot_pareto_fronts


def get_parameters():
    parameters = {
        'population_size': get_numeric_parameter('Population size', int),

        'max_number_of_generations': get_numeric_parameter('Number of generations', int),

        'crossover_probability': get_numeric_parameter('Crossover probability', float),
        'mutation_probability': get_numeric_parameter('Mutation probability', float),
    }

    distances = load_data('distances.csv')
    costs = load_data('costs.csv')

    parameters['genome_size'] = len(costs)
    parameters['problem'] = Problem(costs, distances)

    print('')

    return parameters


def run_analysis_problem():
    fronts = []

    for i in range(3):
        print('\nRun %d' % (i+1))

        parameters = get_parameters()

        fronts.append((
            MOEA(parameters).run()['population'].fronts[0],
            parameters
        ))

    plot_pareto_fronts(fronts)


def run_problem(analysis):
    parameters = get_parameters()

    population = MOEA(parameters).run(analysis)['population']

    print('')

    if get_boolean_parameter('Show whole population'):
        plot_single_run(population.population, 'Whole population', 'Population')

    if get_boolean_parameter('Show Pareto front'):
        plot_single_run(population.fronts[0], 'Pareto front', 'Pareto front')


def main():
    analysis = get_boolean_parameter('Run analysis')

    if analysis and get_boolean_parameter('Multiple runs'):
        run_analysis_problem()
    else:
        run_problem(analysis)


if __name__ == '__main__':
    main()
