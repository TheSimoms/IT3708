from common.ea.utils import random_probability, random_list_position


def genome_swap_mutation(**kwargs):
    genome = list(kwargs.get('genome'))

    if random_probability(kwargs.get('probability')):
        random_position = random_list_position(genome)
        other_position = genome.index(genome[random_position])

        genome[random_position], genome[other_position] = genome[other_position], genome[random_position]

    return genome
