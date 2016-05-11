from random import randint, sample

from common.ea.utils import random_probability


def reverse_sequence_mutation(**kwargs):
    genome = list(kwargs.get('genome'))

    if random_probability(kwargs.get('probability')):
        start, end = list(sorted(sample(range(len(genome)), 2)))

        return genome[:start] + list(reversed(genome[start:end])) + genome[end:]

    return genome


def crossover(pair, crossover_probability, crossover_function):
    genome_a, genome_b = pair[0].genome, pair[1].genome

    if random_probability(crossover_probability):
        return crossover_function(genome_a, genome_b)
    else:
        return genome_a, genome_b


def ordered_crossover(genome_a, genome_b):
    genome_size = len(genome_a)

    crossover_points = sorted(sample(range(genome_size), randint(genome_size // 10, genome_size // 5)))

    parents = [genome_a, genome_b]
    children = [[None] * genome_size for _ in range(2)]

    reverse = False

    for i in range(genome_size):
        child_index = int(reverse)

        children[child_index][i] = parents[child_index][i]

        if i in crossover_points:
            reverse = not reverse

    for child_index in range(2):
        missing = [gene for gene in parents[child_index-1] if gene not in children[child_index]]

        for i in range(genome_size):
            if children[child_index][i] is None:
                children[child_index][i] = missing.pop(0)

    return children
