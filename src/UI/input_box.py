from readline import insert_text
from src.ui_element import UIElement
from src.input_data import InputData
from src.scene import Scene
from src.UI.text import TextElement
import pygame as pg
from src.constants import PALLETTE
from src.utils import Timer


class InputBoxElement(UIElement):
    def __init__(self, formatting_file_path, font):
        super().__init__(formatting_file_path)
        self.text = TextElement(self.information["info"]["input_text_pos"], "", font)

        self.focused = False
        self.insert_position = 0

        self.blinker = Timer([0.5], True)
        self.blink = True

        self.locked = False
    
    def update_element(self, input_data: InputData, parent_scene: Scene):
        if self.information["info"]["hitbox"].collidepoint(input_data.mouse_pos):
            input_data.add_to_cursor_queue(pg.SYSTEM_CURSOR_HAND)

        if input_data.just_released:
            if self.information["info"]["hitbox"].collidepoint(input_data.click_origin) and self.information["info"]["hitbox"].collidepoint(input_data.release_pos):
                self.focused = True
                self.insert_position = len(self.text.text)
            else:
                self.focused = False
                self.blink = True
        
        if self.focused and not self.locked:
            if input_data.key_just_pressed:
                if input_data.key_pressed  == 8:  # backspace
                    if len(self.text.text) > 0:
                        self.text.text = self.text.text[:self.insert_position-1] + self.text.text[self.insert_position:]
                        input_data.reset_key_event()
                        self.text = TextElement(self.information["info"]["input_text_pos"], self.text.text, self.text.font)
                        self.insert_position -= 1

                elif input_data.key_pressed == 1073741904:  # left arrow key
                    self.insert_position -= (1 if self.insert_position > 0 else 0)

                elif input_data.key_pressed == 1073741903:  # right arrow key
                    self.insert_position += (1 if self.insert_position < len(self.text.text) else 0)

                elif input_data.key_unicode_pressed in self.text.font.chars:
                    if len(self.text.text) < self.information["info"]["input_max_len"]:
                        self.text.text = self.text.text[:self.insert_position] + input_data.key_unicode_pressed + self.text.text[self.insert_position:]
                        self.text = TextElement(self.information["info"]["input_text_pos"], self.text.text, self.text.font)
                        self.insert_position += len(input_data.key_unicode_pressed)
                        input_data.reset_key_event()

    def render(self, destination: pg.Surface, dt):
        for element in self.information["elements"]:
            if element[0] not in ['!', '.']:
                self.sprite_surface.blit(self.information["elements"][element][0], self.information["elements"][element][1])
        
        if self.focused:
            text_size = self.text.font.get_surf_length(self.text.text[:self.insert_position])
            start_pos = text_size[0] + self.information["info"]["input_text_pos"][0] - 1, self.information["info"]["input_text_pos"][1]
            end_pos = text_size[0] + self.information["info"]["input_text_pos"][0] - 1, text_size[1] + self.information["info"]["input_text_pos"][1]

            if self.blinker.tick(dt):
                self.blink = not self.blink

            if self.blink:
                pg.draw.line(self.sprite_surface, PALLETTE["white"], start_pos, end_pos)
        
        self.text.render(self.sprite_surface, dt)
        destination.blit(self.sprite_surface, self.information["info"]["position"])

