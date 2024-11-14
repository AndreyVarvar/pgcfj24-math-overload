from operator import truediv
import pygame as pg


class InputData():
    def __init__(self):
        # A data holding class to keep all the data in one place.
        self.mouse_pos: tuple[int, int]


    def update(self, events):
        self.mouse_pos = pg.mouse.get_pos()

