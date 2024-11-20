import json
import pygame as pg
from src.input_data import InputData
from src.scene import Scene
from src.utils import Timer


class UIElement():
    def __init__(self, formatting_file_path):
        self.sprite_surface: pg.Surface
        self.information = self.apply_formatting(formatting_file_path)
    
    def load_formatting(self, formatting_file_path) -> dict:
        
        with open(formatting_file_path, 'r') as file:
            data = json.load(file)
        
        return data
        
    def apply_formatting(self, formatting_file_path):
        if formatting_file_path is None:
            return {}, {}
        
        formatting = self.load_formatting(formatting_file_path)

        textures = {}
        information = {}


        for criteria in formatting:
            if criteria == "textures":
                for texture in formatting["textures"]:
                    textures.update({texture: pg.image.load(formatting['textures'][texture]).convert_alpha()})
            
            elif criteria == "elements":
                information["elements"] = {}
                for element in formatting["elements"]:
                    _from = formatting["elements"][element]["uv"]["from"]
                    _to =  formatting["elements"][element]["uv"]["to"]
                    _to = (_to[0] - _from[0]+1, _to[1] - _from[1]+1)

                    subsurface_rect =  (_from, _to)

                    texture = textures[formatting["elements"][element]["texture"]].subsurface(subsurface_rect)
                    offset = formatting["elements"][element]["at"]
                    information["elements"].update({element: (texture, offset)})

            elif criteria == "uielement":
                information["uielement"] = {}
                information["uielement"]["position"] = pg.Vector2(formatting[criteria]["position"])
                self.sprite_surface = pg.Surface(formatting[criteria]["size"], pg.SRCALPHA)

                _from = formatting[criteria]["hitbox"]["from"]
                _to =  formatting[criteria]["hitbox"]["to"]
                information["uielement"]["hitbox"] = pg.Rect(_from[0], _from[1], _to[0] - _from[0]+1, _to[1] - _from[1]+1)
            
            elif criteria == "interpolation":
                information["interpolation"] = {}
                information["interpolation"]["points"] = [pg.Vector2(point) for point in formatting["interpolation"]["points"]]
                information["interpolation"]["current"] = formatting["interpolation"]["current"]
                information["interpolation"]["time"] = formatting["interpolation"]["time"]
                information["interpolation"]["time_lapsed"] = 0
            
            elif not self.load_element_specific_criteria(information, formatting, criteria):  # criteria not knows by the element as well
                print("ERR: Unknown criteria:", criteria)
    

        return information
    
    def render(self, destination: pg.Surface):
        pass

    def update(self, input_data: InputData, parent_scene: Scene, dt):
        self.update_element(input_data, parent_scene)

    def update_element(self, input_data: InputData, parent_scene: Scene):
        pass

    def load_element_specific_criteria(self, information, formatting, criteria) -> bool:
        pass

    def get_hitbox(self):
        hitbox = self.information["uielement"]["hitbox"].copy()
        hitbox = hitbox.move(self.information["uielement"]["position"])
        return hitbox
    
    def interpolate(self, dt):
        next_index = self.information["interpolation"]["current"] + 1
        if next_index >= len(self.information["interpolation"]["points"]):
            next_index = 0

        self.information["interpolation"]["time_lapsed"] += dt
        ratio = self.information["interpolation"]["time_lapsed"] / self.information["interpolation"]["time"]

        if ratio >= 1:
            self.information["interpolation"]["current"] += 1
            self.information["interpolation"]["time_lapsed"] -= self.information["interpolation"]["time"]
            if self.information["interpolation"]["current"] >= len(self.information["interpolation"]["points"]):
                self.information["interpolation"]["current"] = 0
            self.information["uielement"]["position"] = self.information["interpolation"]["points"][self.information["interpolation"]["current"]].copy()
            return True
        else:
            self.information["uielement"]["position"] = pg.math.Vector2.smoothstep(self.information["interpolation"]["points"][self.information["interpolation"]["current"]], self.information["interpolation"]["points"][next_index], ratio)
            return False

