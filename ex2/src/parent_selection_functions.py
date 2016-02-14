from random import random, choice, sample
from math import sqrt

from .utils import get_fitness


def fitness_proportionate(**kwargs):
    population = kwargs.get('population')
    total_fitness = sum(get_fitness(individual) for individual in population)

    return roulette(
        population=population,
        scaling=lambda individual: get_fitness(individual) / total_fitness
    )


def sigma_scaling(**kwargs):
    population = kwargs.get('population')

    average_fitness = sum(get_fitness(individual) for individual in population) / len(population)
    deviation = sqrt(
        sum((get_fitness(individual) - average_fitness) ** 2 for individual in population) / len(population)
    )

    def expected_value(individual):
        if deviation == 0:
            return 1

        return 1 + ((get_fitness(individual) - average_fitness) / (2 * deviation))

    total_expected_value = sum(expected_value(individual) for individual in population)

    return roulette(
        population=population,
        scaling=lambda individual: expected_value(individual) / total_expected_value
    )


def tournament_selection(**kwargs):
    population = kwargs.get('population')
    group_size = kwargs.get('group_size')
    epsilon = kwargs.get('epsilon')

    def select_from_group(group):
        if random() < epsilon:
            return choice(group)

        return max(group, key=get_fitness)

    pairs = []

    for _ in range(len(population) // 2):
        tournament_pool = list(population)

        tournament_group = sample(tournament_pool, group_size)
        individual_a = select_from_group(tournament_group)

        tournament_pool.remove(individual_a)

        tournament_group = sample(tournament_pool, group_size)
        individual_b = select_from_group(tournament_group)

        pairs.append((individual_a, individual_b))

    return pairs


def uniform_selection(**kwargs):
    return roulette(
        population=kwargs.get('population'),
        scaling=lambda individual: 1 / len(kwargs.get('population'))
    )


def roulette(population, scaling):
    roulette_pool = list(population)

    def roll():
        roulette_candidates = sorted(
            list((individual, scaling(individual)) for individual in roulette_pool),
            key=lambda individual: individual[1]
        )

        roulette_wheel = dict()
        last_value = 0.0

        for individual, p in roulette_candidates:
            roulette_wheel[last_value+p] = individual

            last_value += p

        pair = []

        while len(pair) < 2:
            roulette_ball_position = random()

            for position in roulette_wheel:
                if position >= roulette_ball_position:
                    individual = roulette_wheel[position]

                    if individual not in pair:
                        pair.append(individual)
                        roulette_pool.remove(individual)

                    break

    pairs = []

    for _ in range(len(population) // 2):
        pairs.append(roll())

    return pairs