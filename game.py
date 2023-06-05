import pygame
import pygame as pg
import os
import sys
import random
from settings import *
from player import Player


class Game:
    # Creating and running game
    def __init__(self):
        pg.init()

        self.textures = {}
        self.sounds = {}

        self.load_textures()
        self.load_sounds()

        self.screen = pg.display.set_mode(SCREEN_RESOLUTION)
        self.surface = pg.Surface(DRAW_RESOLUTION)

        self.clock = pg.time.Clock()
        self.dt = 1

        self.player = Player(self.surface)
        self.run()

    # Loading textures
    def load_textures(self):
        for t in os.listdir("content/textures"):
            texture = pg.image.load("content/textures/" + t)
            self.textures[t.replace(".png", "")] = texture

    # Loading sounds
    def load_sounds(self):
        pass
        # for s in os.listdir("content/sounds"):
        #     sound = pg.mixer.Sound("content/sounds/" + s)
        #     self.sounds[s.replace(".wav", "")] = sound

    # Running game
    def run(self):
        while True:
            self.check_events()
            self.check_inputs()
            self.draw()
            self.refresh()

    # Checking events
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.close()

    # Checking input
    def check_inputs(self):
        keys = pg.key.get_pressed()
        self.player.move(keys, self.dt)

    # Drawing on surface
    def draw(self):
        self.surface.blit(self.textures['background'], (0, 0))
        self.player.draw()

    # Refreshing screen
    def refresh(self):
        scaled = pg.transform.scale(self.surface, SCREEN_RESOLUTION)
        self.screen.blit(scaled, (0, 0))
        pg.display.update()
        self.dt = self.clock.tick(FPS) * FPS / 1000

    # Ending the game
    def close(self):
        pg.quit()
        sys.exit(0)
