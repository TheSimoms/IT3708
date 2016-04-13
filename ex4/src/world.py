from random import randint

from ex4.src.constants import MIN_OBJECT_WIDTH, MAX_OBJECT_WIDTH


class Object:
    def __init__(self, x, y, width):
        self.x_start = x
        self.y = y

        self.width = width

    @property
    def x_end(self):
        return self.x_start + self.width - 1

    @property
    def spanning_columns(self):
        return list(range(self.x_start, self.x_end + 1))


class World:
    def __init__(self, dimensions):
        self.dimensions = self.width, self.height = dimensions

        self.object = None

    def generate_new_object(self):
        object_width = randint(MIN_OBJECT_WIDTH, MAX_OBJECT_WIDTH)

        self.object = Object(randint(0, self.width - object_width), self.height, object_width)

    def drop_object(self):
        self.object.y = 0
