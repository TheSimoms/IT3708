import logging

from constants import *
from utils import add_values


class Agent:
    def __init__(self, world, position, direction):
        self.world = world

        self.x, self.y = position
        self.direction = direction

        self.eaten_food_count = 0
        self.eaten_poison_count = 0

        self.total_food_count = self.world.get_value_count(FOOD)
        self.total_poison_count = self.world.get_value_count(POISON)

    @property
    def position(self):
        return self.x, self.y

    @property
    def direction_left(self):
        return DIRECTIONS[(DIRECTIONS.index(self.direction) + 1) % len(DIRECTIONS)]

    @property
    def direction_right(self):
        return DIRECTIONS[DIRECTIONS.index(self.direction) - 1]

    @property
    def coordinate_ahead(self):
        return self.world.get_tile_absolute_coordinates(
            *add_values(self.position, DIRECTION_VALUES[self.direction])
        )

    @property
    def coordinate_left(self):
        return self.world.get_tile_absolute_coordinates(
            *add_values(self.position, DIRECTION_VALUES[self.direction_left])
        )

    @property
    def coordinate_right(self):
        return self.world.get_tile_absolute_coordinates(
            *add_values(self.position, DIRECTION_VALUES[self.direction_right])
        )

    @property
    def current_tile_value(self):
        return self.world.get_tile_value(self.x, self.y)

    @property
    def score(self):
        return (self.eaten_food_count / (self.eaten_food_count + self.world.get_value_count(FOOD))) - \
               (self.eaten_poison_count / (self.eaten_poison_count + self.world.get_value_count(POISON)))

    def move_forward(self):
        self.x, self.y = self.coordinate_ahead

        if self.current_tile_value == FOOD:
            self.eaten_food_count += 1
        elif self.current_tile_value == POISON:
            self.eaten_poison_count += 1

        self.world.set_tile_value(self.x, self.y, EMPTY)

    def turn_left(self):
        self.direction = self.direction_left

    def turn_right(self):
        self.direction = self.direction_right

    def get_sensor_readings(self):
        return {
            MOVE_FORWARD: self.world.get_tile_value(*self.coordinate_ahead),
            MOVE_LEFT: self.world.get_tile_value(*self.coordinate_left),
            MOVE_RIGHT: self.world.get_tile_value(*self.coordinate_right)
        }

    def perform_move(self, move):
        if move not in AGENT_MOVES:
            logging.error('Illegal move received: %s' % move)

            return

        if move == MOVE_FORWARD:
            self.move_forward()
        elif move == MOVE_LEFT:
            self.turn_left()
            self.move_forward()
        elif move == MOVE_RIGHT:
            self.turn_right()
            self.move_forward()
