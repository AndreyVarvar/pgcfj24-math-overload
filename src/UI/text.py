from src.ui_element import UIElement
from src.input_data import InputData
from src.scene import Scene
from src.font import Font
import pygame as pg



class TextElement(UIElement):
    def __init__(self, position, text: str, font: Font):
        super().__init__(position, None)
        self.text_image = font.render(text)
        self.text = text
        self.font = font
    
    def render(self, destination: pg.Surface, dt):
        destination.blit(self.text_image, self.position)
    
    def update(self, input_data: InputData, parent_scene: Scene):
        pass
