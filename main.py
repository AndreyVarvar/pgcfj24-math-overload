import pygame as pg

from src.input_data import InputData
from src.scene import Scene
from src.graph import Graph

pg.init()


class Game():
    def __init__(self):
        self.window = pg.display.set_mode([640, 640])
        self.screen = pg.Surface((64, 64), pg.SRCALPHA)

        self.input_data = InputData()

        self.running = True

        self.clock = pg.time.Clock()
        self.FPS = 64

        self.scenes = {
            "game": Scene({
                "graph element": Graph()
            })
        }

        self.current_scene = self.scenes["game"]

    
    def run(self):
        while self.running:
            dt = self.clock.tick(self.FPS)/1000

            pg.display.set_caption(str(round(1/dt)))

            self.handle_events()
            self.update()
            self.render(dt)

        pg.quit()

    def render(self, dt):
        self.window.fill((240, 240, 240))
        self.screen.fill((240, 240, 240))

        for element in self.current_scene.elements:
            self.current_scene.elements[element].render(self.screen)


        self.window.blit(pg.transform.scale_by(self.screen, 10), (0, 0))

        pg.display.update()
    
    def update(self):
        self.current_scene.update(self.input_data)

    def handle_events(self):
        events = pg.event.get()
        self.input_data.update(events)

        for event in events:
            if event.type == pg.QUIT:
                self.running = False


Game().run()
