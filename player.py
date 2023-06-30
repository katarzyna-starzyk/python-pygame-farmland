import os
import pygame as pg
from settings import *
from tiles import *


class Player(pg.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()

        self.images = {}
        self._textures(surface)

        self.status = "s-stand"
        self.current = 0
        self.moving = True
        self.level = None

        self.image = self.images[self.status][self.current]
        self.rect = self.image.get_rect()

        self.rect.x = DRAW_WIDTH//2
        self.rect.y = DRAW_HEIGHT//2

    def _textures(self, surface):
        folders = sorted(os.listdir("content/textures/player/"))

        for folder in folders:
            self.images[folder] = []
            path = "content/textures/player/" + folder + "/"
            files = sorted(os.listdir(path))

            for file in files:
                self.images[folder].append(pg.image.load(os.path.join(path, file)).convert_alpha(surface))

    def _events(self, keys):
        if self.moving:
            if keys[pg.K_d] or keys[pg.K_a] or keys[pg.K_w] or keys[pg.K_s]:
                if keys[pg.K_w]:
                    self.status = 'w-move'
                    self.level.terrain.move(0, SPEED)
                    if self._collisions():
                        self.level.terrain.move(0, -SPEED)
                elif keys[pg.K_s]:
                    self.status = 's-move'
                    self.level.terrain.move(0, -SPEED)
                    if self._collisions():
                        self.level.terrain.move(0, SPEED)

                if keys[pg.K_d]:
                    self.status = 'd-move'
                    self.level.terrain.move(-SPEED, 0)
                    if self._collisions():
                        self.level.terrain.move(SPEED, 0)
                elif keys[pg.K_a]:
                    self.status = 'a-move'
                    self.level.terrain.move(SPEED, 0)
                    if self._collisions():
                        self.level.terrain.move(-SPEED, 0)
            else:
                self.status = self.status[0] + '-stand'

    def update(self, keys):
        self._events(keys)
        self._animate()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def _animate(self):
        if self.status[2:] == 'move':
            self.current += 0.5

            if self.current >= len(self.images[self.status]):
                self.current = 0

            self.image = self.images[self.status][int(self.current)]
        else:
            self.image = self.images[self.status][0]

    def _collisions(self):
        if pg.sprite.spritecollide(self, self.level.ocean.sprites(), False) \
                or pg.sprite.spritecollide(self, self.level.trees.sprites(), False):
            return True
        else:
            return False


