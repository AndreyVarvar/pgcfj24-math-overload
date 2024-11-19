from src.ui_element import UIElement
from src.input_data import InputData
from src.scene import Scene
import pygame as pg


class ButtonElement(UIElement):
    def __init__(self, format_json_path):
        super().__init__(format_json_path)

        self.is_clicked = False  # clicked and still holding
        self.is_hovered = False

        self.was_clicked = False  # clicked and released
        self.disabled = False  # block the mouse from being used
    
    def render(self, destination, dt):
        self.sprite_surface.fill((0, 0, 0, 0))  # clear the sprite

        for element in self.information["elements"]:
            if element[0] != "!":  # '!' means 'special usage'
                self.sprite_surface.blit(self.information["elements"][element][0], self.information["elements"][element][1])
        
        if self.disabled:
            self.sprite_surface.blit(self.information["elements"]["!on_button_disabled"][0], self.information["elements"]["!on_button_disabled"][1])
        elif self.is_clicked:
            self.sprite_surface.blit(self.information["elements"]["!on_button_click"][0], self.information["elements"]["!on_button_click"][1])
        elif self.is_hovered:
            self.sprite_surface.blit(self.information["elements"]["!on_button_hover"][0], self.information["elements"]["!on_button_hover"][1])
        else:
            self.sprite_surface.blit(self.information["elements"]["!on_button_normal"][0], self.information["elements"]["!on_button_normal"][1])

        destination.blit(self.sprite_surface, self.information["info"]["position"])

    def update_element(self, input_data: InputData, parent_scene: Scene):
        if self.information["info"]["hitbox"].collidepoint(input_data.mouse_pos):
            self.is_hovered = True
            input_data.add_to_cursor_queue(pg.SYSTEM_CURSOR_HAND)
        
            if input_data.mouse_pressed[0] and self.information["info"]["hitbox"].collidepoint(input_data.click_origin):
                self.is_clicked = True
                input_data.reset_mouse_event()
            else:
                self.is_clicked = False
        else:
            self.is_hovered = False
            self.is_clicked = False

        self.was_clicked = False
        if self.information["info"]["hitbox"].collidepoint(input_data.mouse_pos) and not self.disabled:
            if input_data.just_released:
                if self.information["info"]["hitbox"].collidepoint(input_data.click_origin) and self.information["info"]["hitbox"].collidepoint(input_data.release_pos):
                    self.was_clicked = True

