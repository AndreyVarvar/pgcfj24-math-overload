import pygame as pg

from src.input_data import InputData
from src.scene import Scene
from src.graph import Graph
from src.font import Font
from src.constants import *

from src.UI.button import ButtonElement
from src.UI.input_box import InputBoxElement

pg.init()


class Game():
    def __init__(self):
        self.window = pg.display.set_mode([640, 640])
        self.screen = pg.Surface((64, 64), pg.SRCALPHA)

        self.input_data = InputData()

        self.running = True

        self.clock = pg.time.Clock()
        self.FPS = 64*64

        self.font = Font("assets/formatting/mathematica_font.json")

        self.scenes = {
            "game": Scene({
                "graph element": Graph(),
                "start graphing button": ButtonElement((49, 49), "assets/formatting/game/start_graphing_button.json"),
                "graph input box": InputBoxElement((0, 0), "assets/formatting/game/formula_input_box.json", self.font)
            })
        }

        self.current_scene = self.scenes["game"]

    
    def run(self):
        while self.running:
            dt = self.clock.tick(self.FPS)/1000 + 0.001  # to avoid 'division by 0' error

            pg.display.set_caption(str(round(1/dt)))

            self.handle_events()
            self.update()
            self.render(dt)

        pg.quit()

    def render(self, dt):
        self.window.fill(PALLETTE["white"])
        self.screen.fill(PALLETTE["white"])

        for element in self.current_scene.elements:
            self.current_scene.elements[element].render(self.screen, dt)


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

