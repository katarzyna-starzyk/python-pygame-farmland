import random

import pygame as pg
from tiles import *

LIGHTYELLOW = pg.color.THECOLORS['lightyellow']
DARKGREEN = pg.color.THECOLORS['darkgreen']


class Text:
    def __init__(self, text, text_color, px, py, font_type=None, font_size=74):
        self.text = str(text)
        font = pg.font.SysFont(font_type, font_size)
        self.image = font.render(self.text, True, text_color)
        self.rect = self.image.get_rect()
        self.rect.center = px, py

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Fish(pg.sprite.Sprite):
    def __init__(self, ocean):
        super().__init__()
        self.image = pg.image.load("content/textures/fishing/fish.png")
        self.rect = self.image.get_rect()
        random_tile = random.choice(ocean.sprites())
        self.rect.x = random_tile.rect.x
        self.rect.y = random_tile.rect.y

    def update(self):
        self.rect.x -= SPEED

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Level:

    def __init__(self, player, tmx):
        # self.camera_rect = pg.Rect(0, 0, DRAW_WIDTH, DRAW_HEIGHT)
        self.player = player
        self.terrain = TileMap(tmx)
        self.fishes = pg.sprite.Group()

        self.ocean = self.terrain.layers["ocean"]
        self.beach = self.terrain.layers["beach"]
        self.trees = self.terrain.layers["trees"]
        self.bridge = self.terrain.layers["bridge"]
        self.fish_points = 0
        self.text_fishes = Text(self.fish_points, LIGHTYELLOW, 16, 16, font_size=32)

    def update(self, pos):
        self.terrain.update()
        if len(self.fishes) < 5:
            self.fishes.add(Fish(self.ocean))
        self.fishes.update()

        for fish in self.fishes:

            if fish.rect.collidepoint(pos):
                fish.kill()
                self.fish_points += 1

            elif fish.rect.left < 0:
                fish.kill()

            elif fish.rect.right > DRAW_WIDTH:
                fish.kill()

            elif pg.sprite.spritecollide(fish, self.beach.sprites(), False) \
                    or pg.sprite.spritecollide(fish, self.trees.sprites(), False)\
                    or pg.sprite.spritecollide(fish, self.bridge.sprites(), False):
                fish.kill()

        self.text_fishes = Text(self.fish_points, LIGHTYELLOW, 16, 16, font_size=32)

    def draw(self, surface):
        self.terrain.draw(surface)
        self.fishes.draw(surface)
        self.text_fishes.draw(surface)

