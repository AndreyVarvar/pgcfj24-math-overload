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


            elif criteria == "info":
                information["info"] = {}
                for info in formatting["info"]:
                    if formatting["info"][info]["type"] == "preserve":
                        information["info"].update({info: formatting["info"][info]["value"]})

                    elif formatting["info"][info]["type"] == "vector2":
                        information["info"].update({info: pg.Vector2(formatting["info"][info]["value"])})

                    elif formatting["info"][info]["type"] == "rect tlbr":
                        _from = formatting["info"][info]["from"]
                        _to = formatting["info"][info]["to"]

                        if "relative" in formatting["info"][info]["special"]:
                            _from[0] += formatting["info"]["position"]["value"][0]
                            _from[1] += formatting["info"]["position"]["value"][1]
                            _to[0] += formatting["info"]["position"]["value"][0]
                            _to[1] += formatting["info"]["position"]["value"][1]

                        rect = pg.Rect(_from[0], _from[1], _to[0]-_from[0]+1, _to[1]-_from[1]+1)
                        information["info"].update({info: rect})

                    elif formatting["info"][info]["type"] == "list vector2":
                        information["info"][info] = []
                        for value in formatting["info"][info]["values"]:
                            information["info"][info].append(pg.Vector2(value))
                    
                    elif formatting["info"][info]["type"] == "surface":
                        information["info"][info] = {}
                        information["info"][info]["size"] = pg.Vector2(formatting["info"][info]["size"])
                        information["info"][info]["flags"] = []

                        for flag in formatting["info"][info]["flags"]:
                            information["info"][info]["flags"].append(get_flag(flag))

                        self.sprite_surface = pg.Surface(information["info"][info]["size"], get_bitwise_or_of_list(information["info"][info]["flags"]))

                    else:
                        print(f"FORMATTING ERROR: unknown type '{formatting['info'][info]['type']}.'")
            else:
                information[criteria] = {}
                for entry in formatting[criteria]:
                    information[criteria].update({entry: formatting[criteria][entry]})
    

        return information
    
    def render(self, destination: pg.Surface):
        pass

    def update(self, input_data: InputData, parent_scene: Scene, dt):
        # if self.can_interpolate and self.interpolate:
        #     self.interpolation_timer.tick(dt)

        #     self.position[0] = pg.math.smoothstep(self.original_position[0], self.other["info"]["interpolation_dest"][0], self.interpolation_timer.percent)
        #     self.position[1] = pg.math.smoothstep(self.original_position[1], self.other["info"]["interpolation_dest"][1], self.interpolation_timer.percent)

        #     if self.interpolation_timer.percent >= 1:
        #         self.other["info"]["interpolation_dest"], self.original_position = self.original_position, self.other["info"]["interpolation_dest"]
        #         self.interpolate = False
        #         self.interpolation_timer.reset()

        self.update_element(input_data, parent_scene)

    def update_element(self, input_data: InputData, parent_scene: Scene):
        pass



def get_flag(s: str):
    if s == "alpha":
        return pg.SRCALPHA

def get_bitwise_or_of_list(l: list):
    b = l[0]
    for i in l[1:]:
        b = b | i
    return b
