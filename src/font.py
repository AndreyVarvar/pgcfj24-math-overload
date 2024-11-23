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
        self.line_spacing = formatting["line spacing"]

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
    
    def render(self, text: str, shadow=False):
        if "not casesensitive" in self.special:
            text = text.lower()
        
        if "no space" in self.special:
            text = text.replace(" ", "")
        
        # first, calculate to size of the surface we'll need
        surf_size = self.get_surf_length(text)
        
        # second, draw all the characters on the surface
        surf = pg.Surface(surf_size, pg.SRCALPHA)
        
        top = 0
        for line in text.split("\n"):
            left = 0  # what's the position of the next char
            line_height = 0
            for c in line:
                if c not in self.chars.keys():
                    c = "unknown"
                
                surf.blit(self.chars[c], [left, top])
                left += self.chars[c].get_rect().width + self.spacing
                line_height = max(line_height, self.chars[c].get_rect().height)

            top += line_height + self.line_spacing
        
        if shadow:
            self.drop_shadow(surf)
        
        return surf

    def get_surf_length(self, text, has_shadow=False):
        surf_size = [0, self.chars["unknown"].get_rect().h]
        for line in text.split("\n"):
            line_height = 0
            line_width = 0
            for c in line:
                if c not in self.chars.keys():
                    c = "unknown"
                
                line_width += self.chars[c].get_rect().width + self.spacing
                line_height = max(surf_size[1], self.chars[c].get_rect().h)
            
            surf_size[0] = max(surf_size[0], line_width)
            surf_size[1] += line_height + self.line_spacing
        
        surf_size[0] += has_shadow
        surf_size[1] += has_shadow
        
        return surf_size

    def drop_shadow(self, text_surf):
        text_mask = pg.mask.from_surface(text_surf)
        mask_surf = pg.Surface(text_surf.get_size())
        for mask in text_mask.connected_components():
            for pixel in mask.outline():
                mask_surf.set_at(pixel, (153, 61, 65))
        mask_surf.set_colorkey((0,0,0))

        surf2 = pg.Surface(text_surf.get_size(), pg.SRCALPHA)
        surf2.blit(text_surf, (0, 0))
        text_surf.blit(mask_surf, (1, 1))
        text_surf.blit(surf2, (0, 0))
