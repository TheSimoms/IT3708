from collections import defaultdict


def load_data(file_path):
    data = defaultdict(lambda: [])

    with open('data/%s' % file_path, 'r') as f:
        for i, row in enumerate(f):
            for distance in [int(column) for column in row.strip().split(',') if len(column)]:
                data[i].append(distance)

    return data
