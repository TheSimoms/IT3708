from numpy import zeros


def normalize_bitstring(bitstring):
    return int(bitstring, base=2) / (2 ** len(bitstring) - 1)


def fill_matrix(data, matrix_dimensions, mapping_function=None):
    matrices = [zeros(dimension) for dimension in matrix_dimensions]

    for matrix in matrices:
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                value = data.pop()

                if mapping_function is not None:
                    value = mapping_function(value)

                matrix[y][x] = value

    return matrices, data


def add_values(*values):
    return tuple(map(sum, zip(*values)))


def scale_value(value, low, high):
    return low + (high - low) * value
