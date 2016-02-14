from utils import flip_bit, list_to_string, random_boolean, random_probability, random_list_position, random_character


def mix_genome(genome_a, genome_b):
    return list_to_string(
        [genome_a[i] if random_boolean() else genome_b[i] for i in range(len(genome_a))]
    )


def splice_genome(genome_a, genome_b):
    if random_boolean():
        genome_a, genome_b = genome_b, genome_a

    splice_position = random_list_position(genome_a)

    return genome_a[:splice_position] + genome_b[splice_position:]


def component_bit_mutation(**kwargs):
    return list_to_string(
        flip_bit(bit) if random_probability(kwargs.get('probability')) else bit for bit in kwargs.get('genome')
    )


def component_string_mutation(**kwargs):
    return list_to_string(
        random_character(kwargs.get('length')) if random_probability(kwargs.get('probability')) else character
        for character in kwargs.get('genome')
    )


def genome_bit_mutation(**kwargs):
    bit_string = list(kwargs.get('genome'))

    if random_probability(kwargs.get('probability')):
        position = random_list_position(bit_string)
        bit_string[position] = flip_bit(bit_string[position])

    return list_to_string(bit_string)


def genome_string_mutation(**kwargs):
    string = list(kwargs.get('genome'))

    if random_probability(kwargs.get('probability')):
        string[random_list_position(string)] = random_character(kwargs.get('length'))

    return list_to_string(string)


def replication(**kwargs):
    return kwargs.get('genome')
