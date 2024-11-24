from hmac import new
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

        self.muted_music = False
        self.muted_sfx = False

        self.music_path = music_path
        self.music_playing = False

        self.quit = False
    
    def update(self, input_data: InputData, sound_manager, dt):
        for element in self.elements:
            self.elements[element].update(input_data, self, sound_manager, dt)  # update every element
        
        if self.music_path is not None and self.music_playing is False:
            pg.mixer.music.load(self.music_path)
            pg.mixer.music.play(-1)
            self.music_playing = True

    def change_scenes(self, new_scene_name):
        self.change_scene = True
        self.new_scene_name = new_scene_name
    
    def reset_scene_change(self):
        self.change_scene = False
        self.new_scene_name = ""
