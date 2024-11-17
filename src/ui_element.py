import json
import pygame as pg
import os
from src.input_data import InputData
from src.scene import Scene


class UIElement():
    def __init__(self, position, formatting_file_path):
        self.position = position
        self.elements = self.apply_formatting(formatting_file_path)

        self.sprite_surface: pg.Surface
        self.hitbox: pg.Rect
    
    def load_formatting(self, formatting_file_path) -> dict:
        
        with open(formatting_file_path, 'r') as file:
            data = json.load(file)
        
        return data
        
    def apply_formatting(self, formatting_file_path):
        if formatting_file_path is None:
            return {}
        
        formatting = self.load_formatting(formatting_file_path)

        self.sprite_surface = pg.Surface(formatting["size"], pg.SRCALPHA)

        textures = {}
        elements = {}

        for criteria in formatting:
            if criteria == "hitbox":
                _from = formatting[criteria]["from"] 
                _to = formatting[criteria]["to"]
                self.hitbox = pg.Rect(_from[0]+self.position[0], _from[1]+self.position[1], _to[0]-_from[0]+1, _to[1]-_from[1]+1)

            elif criteria == "textures":
                for texture in formatting["textures"]:
                    textures.update({texture: pg.image.load(formatting['textures'][texture]).convert_alpha()})
            
            elif criteria == "elements":
                for element in formatting["elements"]:
                    if element[0] == ".":
                        elements.update({element: formatting["elements"][element]})
                    else:
                        _from = formatting["elements"][element]["uv"]["from"]
                        _to =  formatting["elements"][element]["uv"]["to"]
                        _to = (_to[0] - _from[0]+1, _to[1] - _from[1]+1)

                        subsurface_rect =  (_from, _to)

                        texture = textures[formatting["elements"][element]["texture"]].subsurface(subsurface_rect)
                        offset = formatting["elements"][element]["at"]
                        elements.update({element: (texture, offset)})
    

        return elements
    
    def render(self, destination: pg.Surface):
        pass

    def update(self, input_data: InputData, parent_scene: Scene):
        pass
