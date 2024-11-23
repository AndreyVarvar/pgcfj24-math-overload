import pygame as pg
from src.input_data import InputData

class Scene():
    def __init__(self, elements: dict, music_path=None):
        """Base scene class, responsible for handling 

        Args:
            elements (dict): dictionary of all the elements, that are supposed to be handles by the scene class. For example UI elements, 
                                  that need to be updated every frame
        """
        self.change_scene = False
        self.new_scene_name = ""
        self.elements = elements

        self.music_path = music_path
        self.music_playing = False
    
    def update(self, input_data: InputData, dt):
        for element in self.elements:
            self.elements[element].update(input_data, self, dt)  # update every element
        
        if self.music_path is not None and self.music_playing is False:
            pg.mixer.music.load(self.music_path)
            pg.mixer.music.play(-1)
            self.music_playing = True
