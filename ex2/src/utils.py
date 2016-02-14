import random

from string import ascii_letters


def list_to_string(lst):
    return ''.join(lst)


def random_probability(p):
    return random.random() <= p


def random_boolean():
    return bool(random.getrandbits(1))


def random_character(length):
    return random.choice(ascii_letters[:length])


def random_list_position(lst):
    return random.randrange(len(lst))


def random_bits(length):
    return list_to_string(random.getrandbits(length))


def get_fitness(individual):
    return individual.fitness


def flip_bit(bit):
    return '1' if bit == '0' else '1'


def bit_string_to_ints(bit_string):
    return tuple(map(int, bit_string))


def generate_bit_individual(genome_size):
    return random_bits(genome_size)


def generate_bit_population(population_size, genome_size):
    return tuple(generate_bit_individual(genome_size) for _ in range(population_size))


def crossover(pair, crossover_probability, crossover_function, number_of_children=2):
    genome_a, genome_b = pair[0]['genome'], pair[1]['genome']

    children = []

    for _ in range(number_of_children):
        if random.random() > crossover_probability:
            children.append(genome_a if random_boolean() else genome_b)
        else:
            children.append(crossover_function(genome_a, genome_b))

    return tuple(children)
