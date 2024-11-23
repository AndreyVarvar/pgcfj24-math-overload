from src.ui_element import UIElement
from src.UI.text import TextElement
import pygame as pg


class Panel(UIElement):
    def __init__(self, formatting_file_path, font):
        super().__init__(formatting_file_path)
        self.text = TextElement(self.information["panel"]["text_pos"], self.information["panel"]["text"], font)

    def render_element(self, destination: pg.Surface, dt):
        for element in self.information["elements"]:
            if element[0] != '!':
                self.sprite_surface.blit(self.information["elements"][element][0], self.information["elements"][element][1])

        self.text.render(self.sprite_surface, dt)
        destination.blit(self.sprite_surface, self.information["uielement"]["position"])
    
    def load_element_specific_criteria(self, information, formatting, criteria):
        if criteria == "panel":
            information[criteria]["text"] = formatting[criteria]["text"]
            information[criteria]["text_pos"] = formatting[criteria]["text_pos"]
        else:
            return False  # unknown criteria
        
        return True  # aha, criteria known!
    
    def update_text(self, new_text):
        self.text = TextElement(self.information["panel"]["text_pos"], new_text, self.text.font, shadow=True)


