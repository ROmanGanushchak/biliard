import math
from random import randint, choice
import pygame

class Ball:
    def __init__(self, x, y, r, FPS, index_item, color=(255, 0, 0), color_text=(255, 255, 255)):
        self.mk = 0.95
        self.vx, self.vy = 0, 0 #choice([randint(100, 101), randint(-101, -100)]), choice([randint(100, 101), randint(-101, -100)])
        self.mass, self.r, self.FPS, self.index_item, self.color = r, r, FPS, index_item, color
        self.x, self.y = x, y
        self.f = pygame.font.Font(None, r)
        self.text = self.f.render(str(self.index_item), True, color_text)

    def get_edge_points(self):
        return [[self.x + self.r, self.y],
                [self.x, self.y + self.r],
                [self.x - self.r, self.y],
                [self.x, self.y - self.r]]

    def update(self):
        self.x, self.y = self.x + self.vx * 1 / self.FPS, self.y + self.vy * 1 / self.FPS

        self.vx -= self.mk * self.vx * 1 / self.FPS
        self.vy -= self.mk * self.vy * 1 / self.FPS

    def check_in_point(self, x, y):
        return self.r ** 2 >= (x - self.x) ** 2 + (y - self.y) ** 2

    def blit_text(self, sc):
        place = self.text.get_rect(center=(self.x, self.y))
        sc.blit(self.text, place)

class Controls_ball(Ball):
    def __init__(self, x, y, r, FPS):
        super().__init__(x, y, r, FPS, 0, (255, 255, 255), (0, 0, 0))