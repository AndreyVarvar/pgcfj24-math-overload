from src.ui_element import UIElement
from src.input_data import InputData
from src.scene import Scene
from src.font import Font
import pygame as pg
from math import sin



class TextElement(UIElement):
    def __init__(self, position, text: str, font: Font, woble: bool=False):
        super().__init__(None)
        self.position = pg.Vector2(position)
        self.text_image = font.render(text)
        self.text = text
        self.font = font

        self.visible = True

        self.woble = woble  # woble text up and down
        self.time = 0
    
    def render(self, destination: pg.Surface, dt):
        position = self.position.copy()

        if self.woble:
            self.time += dt
            position.y += sin(10*self.time)
        
        if self.visible:
            destination.blit(self.text_image, position)
    
    def update(self, input_data: InputData, parent_scene: Scene, dt):
        pass
