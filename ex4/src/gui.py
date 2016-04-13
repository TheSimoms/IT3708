import pygame

from time import time

from constants import *


LINE_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (255, 255, 255)

AGENT_DEFAULT_COLOR = (0, 0, 255)
AGENT_PULLING_COLOR = (255, 0, 255)

BEER_SAFE_COLOR = (0, 255, 0)
BEER_DANGER_COLOR = (255, 0, 0)

SLEEP_TIME = 1.0
SLEEP_STEP = 0.10
MAX_SLEEP_TIME = 5.0

CELL_SIZE = 50


class GUI:
    def __init__(self, title, agent):
        self.title = title
        self.agent = agent

        self.agent.set_gui(self)

        pygame.init()

        self.paused = True
        self.sleep_time = SLEEP_TIME

        self.window_size = self.width, self.height = \
            self.agent.world.width * CELL_SIZE, self.agent.world.height * CELL_SIZE

        self.window = pygame.display.set_mode(self.window_size)
        self.font = pygame.font.SysFont("comicsansms", 30)

        self.pause()

    def pause(self):
        self.paused = True

        pygame.display.set_caption('%s (Paused)' % self.title)

    def un_pause(self):
        self.paused = False

        pygame.display.set_caption(self.title)

    def draw_board(self):
        self.window.fill(BACKGROUND_COLOR)

        self.window.blit(
            self.font.render('Score: %f' % self.agent.score, True, (0, 0, 0)),
            (10, 50)
        )

        pygame.draw.rect(
            self.window,
            BEER_SAFE_COLOR if self.agent.world.object.width <= 4 else BEER_DANGER_COLOR,
            pygame.Rect(
                self.agent.world.object.x_start * CELL_SIZE,
                (self.agent.world.height - self.agent.world.object.y) * CELL_SIZE,
                self.agent.world.object.width * CELL_SIZE,
                CELL_SIZE
            ))

        agent_color = AGENT_PULLING_COLOR if self.agent.moves[-1] == DROP_OBJECT else AGENT_DEFAULT_COLOR

        pygame.draw.rect(
            self.window,
            agent_color,
            pygame.Rect(
                self.agent.x_start * CELL_SIZE,
                self.agent.world.height * CELL_SIZE - CELL_SIZE,
                TRACKER_WIDTH * CELL_SIZE,
                CELL_SIZE
            ))

        if self.agent.x_end < self.agent.x_start:
            pygame.draw.rect(
                self.window,
                agent_color,
                pygame.Rect(
                    0,
                    self.agent.world.height * CELL_SIZE - CELL_SIZE,
                    (self.agent.x_end + 1) * CELL_SIZE,
                    CELL_SIZE
                ))

        pygame.display.flip()

        sleep_time_end = time() + self.sleep_time

        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.un_pause()
                elif event.type == pygame.KEYDOWN and event.key == pygame.QUIT:
                    return

        while time() < sleep_time_end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.pause()
                    elif event.key == pygame.K_UP:
                        self.sleep_time = max(self.sleep_time - SLEEP_STEP, SLEEP_STEP)
                    elif event.key == pygame.K_DOWN:
                        self.sleep_time = min(self.sleep_time + SLEEP_STEP, MAX_SLEEP_TIME)
