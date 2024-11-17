import json
import pygame as pg


class Font():
    def __init__(self, font_formatting_path):
        self.spacing: int
        self.special = []
        self.chars = self.load_formatting(font_formatting_path)

    def load_formatting(self, font_formatting_path):
        with open(font_formatting_path, 'r') as file:
            formatting = json.load(file)

        chars = {}


        font_image = pg.image.load(formatting["path"]).convert_alpha()

        for special in formatting["special"]:
            self.special.append(special)
        
        self.spacing = formatting["spacing"]

        unknown = pg.Rect(formatting["unknown_character"])
        chars.update({"unknown": font_image.subsurface(unknown)})

        x_offset = unknown.right + 1

        for c in formatting["characters"]:
            if c not in formatting["character_rect"].keys():
                rect = pg.Rect(formatting["character_rect"]["default"])
            else:
                rect = pg.Rect(formatting["character_rect"][c])
            
            rect.x += x_offset
            x_offset += rect.w + 1

            chars.update({c: font_image.subsurface(rect)})
        
        return chars
    
    def render(self, text: str):
        if "not casesensitive" in self.special:
            text = text.lower()
        
        if "no space" in self.special:
            text = text.replace(" ", "")
        
        # first, calculate to size of the surface we'll need
        surf_size = self.get_surf_length(text)
        
        # second, draw all the characters on the surface
        surf = pg.Surface(surf_size, pg.SRCALPHA)
        last = 0
        for c in text:
            if c not in self.chars.keys():
                c = "unknown"
            
            surf.blit(self.chars[c], [last, 0])
            last += self.chars[c].get_rect().width + self.spacing
        
        return surf

    def get_surf_length(self, text):
        surf_size = [0, self.chars["unknown"].get_rect().h]
        for c in text:
            if c not in self.chars.keys():
                c = "unknown"
            
            surf_size[0] += self.chars[c].get_rect().width + self.spacing
            surf_size[1] = max(surf_size[1], self.chars[c].get_rect().h)
        
        return surf_size
