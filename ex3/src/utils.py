from math import exp
from numpy import zeros


def sigmoid_function(x):
    return 1 / (1 + exp(-x))


def step_function(x, threshold=0.5):
    return 1 if x > threshold else 0


def normalize_bitstring(bitstring):
    return int(bitstring, base=2) / (2 ** len(bitstring) - 1)


def fill_matrix(data, matrix_dimensions):
    matrices = [zeros(dimension) for dimension in matrix_dimensions]

    for matrix in matrices:
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                matrix[y][x] = data.pop()

    return matrices


def add_values(*values):
    return tuple(map(sum, zip(*values)))
