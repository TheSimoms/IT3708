from random import randint, sample

from common.ea.utils import random_probability


def genome_swap_mutation(**kwargs):
    genome = list(kwargs.get('genome'))

    for i in range(len(genome)):
        if random_probability(kwargs.get('probability')):
            swap_position = genome.index(genome[i])

            genome[i], genome[swap_position] = genome[swap_position], genome[i]

        return genome


def crossover(pair, crossover_probability, crossover_function):
    genome_a, genome_b = pair[0].genome, pair[1].genome

    if random_probability(crossover_probability):
        return crossover_function(genome_a, genome_b)
    else:
        return genome_a, genome_b


def splice_genome(genome_a, genome_b):
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
