from common.ea.utils import random_probability


def genome_swap_mutation(**kwargs):
    genome = list(kwargs.get('genome'))

    for i in range(len(genome)):
        if random_probability(kwargs.get('probability')):
            swap_position = genome.index(genome[i])

            genome[i], genome[swap_position] = genome[swap_position], genome[i]

        return genome
