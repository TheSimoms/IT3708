from ex4.src.constants import *


class Agent:
    def __init__(self, world, network, weights, number_of_time_steps=NUMBER_OF_TIME_STEPS, width=TRACKER_WIDTH):
        self.world = world
        self.network = network
        self.weights = weights
        self.gui = None

        self.number_of_time_steps = number_of_time_steps

        self.width = width
        self.x_start = 0

        self.points = [0, 0, 0, 0]
        self.moves = []

        self.can_drop_objects = self.network.get_number_of_neurons_in_layer(-1)[0] == 3

    def set_gui(self, gui):
        self.gui = gui

    def reset_position(self):
        self.x_start = (self.world.width // 2) - (self.width // 2)

    @property
    def score(self):
        return sum(map(lambda x: x[0] * x[1], zip(self.points, self.weights)))

    @property
    def x_end(self):
        return (self.x_start + self.width - 1) % self.world.width

    @property
    def spanning_columns(self):
        if self.x_end < self.x_start:
            return list(range(self.x_start, self.world.width)) + list(range(0, self.x_end + 1))

        return list(range(self.x_start, self.x_end + 1))

    @property
    def sensor_readings(self):
        return [(int(i) in self.world.object.spanning_columns) for i in self.spanning_columns]

    def check_object(self, _object):
        object_spanning_columns = set(_object.spanning_columns)
        self_spanning_columns = set(self.spanning_columns)

        if object_spanning_columns.issubset(self_spanning_columns):
            if _object.width >= self.width:
                # Caught big tile
                self.points[2] += 1
            else:
                # Caught small tile
                self.points[0] += 1
        elif object_spanning_columns.intersection(self_spanning_columns):
            if _object.width >= self.width:
                # Avoided big tile
                self.points[1] += 1
            else:
                # Missed small tile
                self.points[3] += 1
        else:
            if _object.width >= self.width:
                # Avoided big tile
                self.points[1] += 1
            else:
                # Missed small tile
                self.points[3] += 1

    def drop_object(self):
        self.world.drop_object()

        self.moves.append(DROP_OBJECT)

    def make_move(self, direction, number_of_steps):
        self.x_start += direction * number_of_steps
        self.x_start %= self.world.width

        self.moves.append(direction * number_of_steps)

    def make_best_move(self):
        output_values = self.network.run_input_values(self.sensor_readings)

        direction = None
        step_size = None

        if self.can_drop_objects and all(output_values[2] > value for value in output_values[:2]):
            self.drop_object()
        elif output_values[0] > output_values[1]:
            direction = LEFT
            step_size = output_values[0] - output_values[1]
        else:
            direction = RIGHT
            step_size = output_values[1] - output_values[0]

        if direction and step_size:
            step_size = max(0, int(step_size * 4.99))

            self.make_move(direction, step_size)

    def run(self):
        self.world.generate_new_object()

        for _ in range(self.number_of_time_steps):
            self.world.object.y -= 1

            if self.world.object.y == 0:
                self.check_object(self.world.object)
                self.world.generate_new_object()

                continue

            self.make_best_move()

            if self.gui is not None:
                self.gui.draw_board()


class AgentWithWalls(Agent):
    def __init__(self, world, network, width=TRACKER_WIDTH):
        super().__init__(world, network, width)

    @property
    def x_end(self):
        return self.x_start + self.width - 1

    def make_move(self, direction, number_of_steps):
        self.x_start += direction * number_of_steps

        self.moves.append(direction * number_of_steps)

        self.x_start = max(self.x_start, 0)
        self.x_start = min(self.x_start, self.world.width - self.width)
