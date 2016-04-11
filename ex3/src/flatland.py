from random import random, choice

from world import World
from agent import Agent

from constants import *


class Flatland(World):
    def __init__(self, dimensions=(10, 10), distributions=(1/3, 1/3), number_of_steps=60, activation_threshold=0.5):
        self.distributions = distributions
        self.number_of_steps = number_of_steps
        self.activation_threshold = activation_threshold

        super().__init__(dimensions)

        self.agent = Agent(self, self.get_random_cell_containing_value(EMPTY), choice(DIRECTIONS))
        
    def generate_tile(self):
        return FOOD if random() < self.distributions[0] else POISON if random() < self.distributions[1] else EMPTY

    def clone(self):
        return Flatland(
            (self.width, self.height), self.distributions, self.number_of_steps, self.activation_threshold
        )

    def run(self, network):
        moves = []

        while self.number_of_steps > 0:
            sensor_readings = self.agent.get_sensor_readings()

            inputs = [
                int(sensor_readings[MOVE_FORWARD] == FOOD),
                int(sensor_readings[MOVE_LEFT] == FOOD),
                int(sensor_readings[MOVE_RIGHT] == FOOD),
                int(sensor_readings[MOVE_FORWARD] == POISON),
                int(sensor_readings[MOVE_LEFT] == POISON),
                int(sensor_readings[MOVE_RIGHT] == POISON),
            ]

            outputs = network.run_inputs(inputs)

            move_index = max(range(len(outputs)), key=lambda i: outputs[i])

            if outputs[move_index] < self.activation_threshold:
                move = NO_OPERATION
            else:
                move = AGENT_MOVES[move_index]

            self.agent.perform_move(move)
            self.number_of_steps -= 1

            moves.append(move)

        return moves
