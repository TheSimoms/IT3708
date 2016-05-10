from random import choice, sample

from common.ea.utils import random_probability


def tournament_selection(**kwargs):
    population = kwargs.get('population')
    group_size = kwargs.get('group_size')
    epsilon = kwargs.get('epsilon')

    def select_from_group(group):
        if random_probability(epsilon):
            return choice(group)

        return sorted(group)[0]

    pairs = []

    while len(pairs) < len(population) / 2:
        tournament_pool = list(population)

        tournament_group = sample(tournament_pool, group_size)
        individual_a = select_from_group(tournament_group)

        tournament_pool.remove(individual_a)

        tournament_group = sample(tournament_pool, group_size)
        individual_b = select_from_group(tournament_group)

        pairs.append((individual_a, individual_b))

    return pairs
