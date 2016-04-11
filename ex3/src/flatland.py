from random import random, choice, randint

from world import World
from agent import Agent

from constants import *


class Flatland(World):
    def __init__(self, dimensions=(10, 10), distributions=(1/3, 1/3), number_of_steps=60, activation_threshold=0.5,
                 agent_position=None):
        self.distributions = distributions
        self.number_of_steps = number_of_steps
        self.activation_threshold = activation_threshold

        if not agent_position:
            agent_position = [randint(0, dimension-1) for dimension in dimensions]

        self.agent = Agent(self, agent_position, choice(DIRECTIONS))

        super().__init__(dimensions)
        
    def generate_map(self):
        temporary_map = [[EMPTY for _ in range(self.width)] for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) == self.agent.position:
                    continue

                if temporary_map[y][x] == EMPTY and random() < self.distributions[0]:
                    temporary_map[y][x] = FOOD

                if temporary_map[y][x] == EMPTY and random() < self.distributions[1]:
                    temporary_map[y][x] = POISON

        return temporary_map

    def clone(self):
        return Flatland(
            (self.width, self.height), self.distributions, self.number_of_steps, self.activation_threshold,
            self.agent.position
        )

    def run(self, network):
        moves = []

        while self.number_of_steps >= 0:
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
