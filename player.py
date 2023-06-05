import pygame as pg
from settings import *


# class Player(pg.Rect):
class Player:

    def __init__(self, screen):
        # super().__init__()
        self.screen = screen

        self.x = DRAW_WIDTH // 2
        self.y = DRAW_HEIGHT // 2
        self.h = 32
        self.w = 16

    def draw(self,):
        pg.draw.rect(self.screen, (180, 0, 180), pg.Rect(self.x, self.y, self.w, self.h))

    def move(self, keys, dt):
        if keys[pg.K_d]:
            self.x += int(round(SPEED * dt))
        if keys[pg.K_a]:
            self.x -= int(round(SPEED * dt))
        if keys[pg.K_w]:
            self.y -= int(round(SPEED * dt))
        if keys[pg.K_s]:
            self.y += int(round(SPEED * dt))

