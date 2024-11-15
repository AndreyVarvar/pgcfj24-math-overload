import pygame as pg
from src.input_data import InputData

class Scene():
    def __init__(self, elements: dict):
        """Base scene class, responsible for handling 

        Args:
            elements (dict): dictionary of all the elements, that are supposed to be handles by the scene class. For example UI elements, 
                                  that need to be updated every frame
        """
        self.change_scene = False
        self.new_scene_name = ""
        self.elements = elements
    
    def update(self, input_data: InputData):
        responses = []

        for element in self.elements:
            responses.append(self.elements[element].update(input_data, self))  # update every element
        
        for response in responses:
            pass  # later
