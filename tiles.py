from pytmx.util_pygame import load_pygame
import pygame as pg
from settings import *


class Tile(pg.sprite.Sprite):

    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Layer(pg.sprite.Group):

    def __init__(self, tmx, layer_name):
        super().__init__()
        self.name = layer_name
        self.layer = tmx.get_layer_by_name(layer_name)

        for x, y, s in self.layer.tiles():
            self.add(Tile(s, x*TILE_SIZE, y*TILE_SIZE))


class Terrain(pg.sprite.Group):

    def __init__(self):
        super().__init__()
        self.tile = pg.Surface((16, 16), pg.SRCALPHA)
        self.layers = {}

    def get_pos(self, pos):
        for tile in self.sprites():
            if tile.rect.collidepoint(pos):
                return tile.rect
        return False


class Ocean(Terrain):

    def __init__(self, tmx):
        super().__init__()
        self.fishing = False
        self.layers = {
            0: Layer(tmx, "Ocean_deep"),
            1: Layer(tmx, "Ocean_medium"),
            2: Layer(tmx, "Ocean_low")
        }

        for layer in self.layers.keys():
            self.add(self.layers[layer])

    def draw_rect(self, pos, surface):
        current_pos = self.get_pos(pos)
        if current_pos:
            self.fishing = True
            pg.draw.rect(self.tile, (0, 0, 0, 16), self.tile.get_rect())
            surface.blit(self.tile, current_pos)
        else:
            self.fishing = False


class Beach(Terrain):

    def __init__(self, tmx):
        super().__init__()
        self.layers = {
            0: Layer(tmx, "Beach_high"),
            1: Layer(tmx, "Beach_low"),
        }

        for layer in self.layers.keys():
            self.add(self.layers[layer])


class Trees(Terrain):

    def __init__(self, tmx):
        super().__init__()
        self.layers = {
            0: Layer(tmx, "Trees")
        }

        for layer in self.layers.keys():
            self.add(self.layers[layer])


class Bridge(Terrain):

    def __init__(self, tmx):
        super().__init__()
        self.layers = {
            0: Layer(tmx, "Bridge")
        }

        for layer in self.layers.keys():
            self.add(self.layers[layer])


class TileMap(pg.sprite.Group):

    def __init__(self, tmx):
        super().__init__()
        # self.layers = {}
        self.layers = {
            "ocean": Ocean(tmx),
            "beach": Beach(tmx),
            "trees": Trees(tmx),
            "bridge": Bridge(tmx)
        }

        for layer in self.layers.keys():
            self.add(self.layers[layer])

    def move(self, x, y):
        for tile in self.sprites():
            tile.rect.move_ip(x, y)
