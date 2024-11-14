import pygame as pg
from src.input_data import InputData

class Scene():
    def __init__(self, name: str, elements: dict):
        """Base scene class, responsible for handling 

        Args:
            name (str): name of the scene. Used to identify the scene when we will need to change to it.
            elements (dict): dictionary of all the elements, that are supposed to be handles by the scene class. For example UI elements, 
                                  that need to be updated every frame
        """
        self.name = name
        self.change_scene = False
        self.new_scene_name = ""
        self.elements = elements
    
    def update(self, input_data: InputData):
        responses = []

        for element in self.elements:
            responses.append(element.update(input_data, self))  # update every element
        
        for response in responses:
            pass  # later
