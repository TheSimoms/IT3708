import pygame

from time import sleep

from constants import *


FOOD_COLOR = (0, 255, 0)
POISON_COLOR = (255, 0, 0)
LINE_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (255, 255, 255)
AGENT_COLOR = (0, 0, 255)
AGENT_SNOUT_COLOR = (255, 255, 0)

SLEEP_TIME = 1.0
SLEEP_STEP = 0.25

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
        pass

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

        for move in self.moves + [NO_OPERATION]:
            self.draw_board()

            while self.paused:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.un_pause()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.QUIT:
                        return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.pause()
                    elif event.key == pygame.K_PLUS:
                        sleep_time = max(sleep_time - SLEEP_STEP, SLEEP_STEP)
                    elif event.key == pygame.K_MINUS:
                        sleep_time += SLEEP_STEP

            sleep(sleep_time)

            self.flatland.agent.perform_move(move)
