import random

from string import ascii_letters


def list_to_string(lst):
    return ''.join(map(str, lst))


def random_probability(p):
    return random.random() <= p


def random_boolean():
    return random.getrandbits(1)


def random_character(character_set_size):
    return random.choice(ascii_letters[:character_set_size])


def random_list_position(lst):
    return random.randrange(len(lst))


def random_string(length, character_set_size):
    return list_to_string(random_character(character_set_size) for _ in range(length))


def random_bits(length):
    return list_to_string(str(random.getrandbits(1)) for _ in range(length))


def crossover(pair, crossover_probability, crossover_function):
    genome_a, genome_b = pair[0].genome, pair[1].genome

    children = []

    for _ in range(2):
        if random_probability(crossover_probability):
            children.append(crossover_function(genome_a, genome_b))
        else:
            children.append(genome_a if random_boolean() else genome_b)

    return tuple(children)


def flip_bit(bit):
    return '1' if bit == '0' else '1'


def bit_string_to_ints(bit_string):
    return tuple(map(int, bit_string))


def generate_bit_individual(genome_size):
    return random_bits(genome_size)


def generate_bit_population(**kwargs):
    return tuple(
        generate_bit_individual(genome_size=kwargs.get('genome_size')) for _ in range(kwargs.get('population_size'))
    )


def generate_string_individual(genome_size, character_set_size):
    return random_string(length=genome_size, character_set_size=character_set_size)


def generate_string_population(**kwargs):
    return tuple(
        generate_string_individual(
            genome_size=kwargs.get('genome_size'),
            character_set_size=kwargs.get('S')
        ) for _ in range(kwargs.get('population_size'))
    )
