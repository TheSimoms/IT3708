from random import choice


class World:
    def __init__(self, dimensions):
        self.width, self.height = dimensions
        self.map = self.generate_map()

    def generate_map(self):
        raise NotImplementedError

    def get_tile_absolute_coordinates(self, x, y):
        return x % self.width, y % self.height

    def get_tile_value(self, x, y):
        return self.map[y][x]

    def set_tile_value(self, x, y, value):
        self.map[y][x] = value

    def get_value_count(self, value):
        return sum(row.count(value) for row in self.map)

    def get_value_coordinates(self, value):
        return list(
            (x, y) for x in range(self.width) for y in range(self.height) if self.get_tile_value(x, y) == value
        )

    def get_random_cell_containing_value(self, value):
        return choice(self.get_value_coordinates(value))
