import pygame

from time import time

from constants import *
from common.utils.utils import add_values


FOOD_COLOR = (0, 255, 0)
POISON_COLOR = (255, 0, 0)
LINE_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (255, 255, 255)
AGENT_COLOR = (0, 0, 255)
AGENT_SNOUT_COLOR = (255, 255, 0)

SLEEP_TIME = 1.0
SLEEP_STEP = 0.10
MAX_SLEEP_TIME = 5.0

CELL_SIZE = 100


class GUI:
    def __init__(self, title, flatland, moves):
        self.title = title

        self.flatland = flatland
        self.moves = moves

        pygame.init()

        self.paused = True

        self.window_size = self.width, self.height = self.flatland.width * CELL_SIZE, self.flatland.height * CELL_SIZE
        self.window = pygame.display.set_mode(self.window_size)

        self.pause()
        self.show_run()

    def pause(self):
        self.paused = True

        pygame.display.set_caption('%s (Paused)' % self.title)

    def un_pause(self):
        self.paused = False

        pygame.display.set_caption(self.title)

    def draw_circle(self, x, y, color, radius=CELL_SIZE//5):
        offset = CELL_SIZE // 2

        pygame.draw.circle(
            self.window,
            color,
            (x * CELL_SIZE + offset, y * CELL_SIZE + offset),
            radius
        )

    def draw_agent(self, x, y):
        self.draw_circle(x, y, AGENT_COLOR, radius=CELL_SIZE//4)

        snout_position = add_values(
            (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2),
            map(
                lambda pos: 20 * pos, DIRECTION_VALUES[self.flatland.agent.direction]
            )
        )

        pygame.draw.circle(
            self.window,
            AGENT_SNOUT_COLOR,
            snout_position,
            CELL_SIZE // 10
        )

    def draw_food(self, x, y):
        self.draw_circle(x, y, FOOD_COLOR)

    def draw_poison(self, x, y):
        self.draw_circle(x, y, POISON_COLOR)

    def draw_board(self):
        self.window.fill(BACKGROUND_COLOR)

        for x in range(-1, self.width, CELL_SIZE):
            pygame.draw.line(self.window, LINE_COLOR, (x, 0), (x, self.height), 2)

        for y in range(-1, self.height, CELL_SIZE):
            pygame.draw.line(self.window, LINE_COLOR, (0, y), (self.width, y), 2)

        for y, row in enumerate(self.flatland.map):
            for x, tile in enumerate(row):
                if (x, y) == self.flatland.agent.position:
                    self.draw_agent(x, y)
                elif tile == FOOD:
                    self.draw_food(x, y)
                elif tile == POISON:
                    self.draw_poison(x, y)

        pygame.display.flip()

    def show_run(self):
        sleep_time = SLEEP_TIME

        for move in self.moves:
            self.draw_board()

            while self.paused:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.un_pause()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.QUIT:
                        return

            sleep_time_end = time() + sleep_time

            while time() < sleep_time_end:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.pause()
                        elif event.key == pygame.K_UP:
                            sleep_time = max(sleep_time - SLEEP_STEP, SLEEP_STEP)
                        elif event.key == pygame.K_DOWN:
                            sleep_time = min(sleep_time + SLEEP_STEP, MAX_SLEEP_TIME)

            self.flatland.agent.perform_move(move)

        input('\nScenario complete. Press enter to continue.')

        pygame.quit()
