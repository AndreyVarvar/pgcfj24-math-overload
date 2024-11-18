import json
import pygame as pg
from src.input_data import InputData
from src.scene import Scene
from src.utils import Timer


class UIElement():
    def __init__(self, position, formatting_file_path):
        self.position = list(position)
        self.original_position = position
        self.elements, self.other = self.apply_formatting(formatting_file_path)

        self.sprite_surface: pg.Surface
        self.hitbox: pg.Rect

        self.interpolate = False
        self.can_interpolate = False
        if "info" in self.other.keys():
            if "interpolation_dest" in self.other["info"].keys():
                self.can_interpolate = True
                self.interpolation_timer = Timer([self.other["info"]["interpolate_time"]], False)
    
    def load_formatting(self, formatting_file_path) -> dict:
        
        with open(formatting_file_path, 'r') as file:
            data = json.load(file)
        
        return data
        
    def apply_formatting(self, formatting_file_path):
        if formatting_file_path is None:
            return {}, {}
        
        formatting = self.load_formatting(formatting_file_path)

        textures = {}
        elements = {}
        other = {}

        for criteria in formatting:
            if criteria == "size":
                self.sprite_surface = pg.Surface(formatting["size"], pg.SRCALPHA)
            elif criteria == "hitbox":
                _from = formatting[criteria]["from"] 
                _to = formatting[criteria]["to"]
                self.hitbox = pg.Rect(_from[0]+self.position[0], _from[1]+self.position[1], _to[0]-_from[0]+1, _to[1]-_from[1]+1)

            elif criteria == "textures":
                for texture in formatting["textures"]:
                    textures.update({texture: pg.image.load(formatting['textures'][texture]).convert_alpha()})
            
            elif criteria == "elements":
                for element in formatting["elements"]:
                    _from = formatting["elements"][element]["uv"]["from"]
                    _to =  formatting["elements"][element]["uv"]["to"]
                    _to = (_to[0] - _from[0]+1, _to[1] - _from[1]+1)

                    subsurface_rect =  (_from, _to)

                    texture = textures[formatting["elements"][element]["texture"]].subsurface(subsurface_rect)
                    offset = formatting["elements"][element]["at"]
                    elements.update({element: (texture, offset)})
            else:
                other[criteria] = {}
                for entry in formatting[criteria]:
                    other[criteria].update({entry: formatting[criteria][entry]})
    

        return elements, other
    
    def render(self, destination: pg.Surface):
        pass

    def update(self, input_data: InputData, parent_scene: Scene, dt):
        if self.can_interpolate and self.interpolate:
            self.interpolation_timer.tick(dt)

            self.position[0] = pg.math.smoothstep(self.original_position[0], self.other["info"]["interpolation_dest"][0], self.interpolation_timer.percent)
            self.position[1] = pg.math.smoothstep(self.original_position[1], self.other["info"]["interpolation_dest"][1], self.interpolation_timer.percent)

            if self.interpolation_timer.percent >= 1:
                self.other["info"]["interpolation_dest"], self.original_position = self.original_position, self.other["info"]["interpolation_dest"]
                self.interpolate = False
                self.interpolation_timer.reset()

        self.update_element(input_data, parent_scene)

    def update_element(self, input_data: InputData, parent_scene: Scene):
        pass
