import sys
import pygame as pg
from pytmx.util_pygame import load_pygame
from settings import *
from tiles import *
from player import *
from level import *


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption("FISHLAND")

        self.screen = pg.display.set_mode(SCREEN_RESOLUTION)
        self.surface = pg.Surface(DRAW_RESOLUTION)
        self.game_running = False

        self.clock = pg.time.Clock()
        self.dt = 0

        self.map_data = load_pygame("content/Map/map.tmx")

        self.player = Player(self.surface)
        self.level = Level(self.player, self.map_data)
        self.player.level = self.level

        # pg.mixer.music.load("content/sounds/music.wav")
        # pg.mixer.music.play(-1)
        self.run()

    def _check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._close()

    def _check_inputs(self):
        pass

    def _update(self, pos):
        keys = pg.key.get_pressed()
        events = pg.event.get()
        self.player.update(keys)
        self.level.update(pos)

    def _draw(self, pos):
        self.level.draw(self.surface)
        self.player.draw(self.surface)

    def _refresh(self):
        scaled = pg.transform.scale(self.surface, SCREEN_RESOLUTION)
        self.screen.blit(scaled, (0, 0))

        pg.display.flip()
        self.dt = self.clock.tick(FPS) / 1000

    @staticmethod
    def _close():
        pg.quit()
        sys.exit(0)

    def menu(self):
        while not self.game_running:
            self.surface.blit(pg.image.load("content/Map/background.png"), (0, 0))

            # title = Text("FishLand", DARKGREEN, DRAW_WIDTH//2, DRAW_HEIGHT//2, font_size=64)
            # title.draw(self.surface)

            bottom = Text("Press any key to continue...", DARKGREEN, DRAW_WIDTH//2, DRAW_HEIGHT - 64, font_size=16)
            bottom.draw(self.surface)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    self.game_running = True
                    break

            self._refresh()

    def run(self):
        while not self.game_running:
            self.menu()
        while self.game_running:
            x, y = pg.mouse.get_pos()
            x /= (SCREEN_HEIGHT / DRAW_HEIGHT)
            y /= (SCREEN_WIDTH / DRAW_WIDTH)
            pos = (x, y)

            self._check_events()
            self._check_inputs()
            self._update(pos)
            self._draw(pos)
            self._refresh()
