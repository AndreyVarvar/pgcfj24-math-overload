import pygame as pg
from src.input_data import InputData
pg.init()


class Game():
    def __init__(self):
        self.window = pg.display.set_mode([640, 640])
        self.screen = pg.Surface((64, 64), pg.SRCALPHA)

        self.input_data = InputData()

        self.running = True

        self.clock = pg.time.Clock()
        self.FPS = 64

    
    def run(self):
        while self.running:
            dt = self.clock.tick(self.FPS)

            self.handle_events()
            self.render(dt)

        pg.quit()

    def render(self, dt):
        self.window.fill((255, 255, 255))
        

        self.window.blit(pg.transform.scale_by(self.screen, 10), (0, 0))

        pg.display.update()

    def handle_events(self):
        events = pg.event.get()
        self.input_data.update(events)

        for event in events:
            if event.type == pg.QUIT:
                self.running = False


Game().run()

