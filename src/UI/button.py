from src.ui_element import UIElement
from src.input_data import InputData
from src.scene import Scene
import pygame as pg


class Button(UIElement):
    def __init__(self, position, format_json_path):
        super().__init__(position, format_json_path)

        self.is_clicked = False  # clicked and still holding
        self.is_hovered = False

        self.was_clicked = False  # clicked and released
        self.disabled = False  # block the mouse from being used
    
    def render(self, destination):
        self.sprite_surface.fill((0, 0, 0, 0))  # clear the sprite

        for element in self.elements:
            if element[0] != "!":  # '!' means 'special usage'
                self.sprite_surface.blit(self.elements[element][0], self.elements[element][1])
        
        if self.disabled:
            self.sprite_surface.blit(self.elements["!on_button_disabled"][0], self.elements["!on_button_disabled"][1])
        elif self.is_clicked:
            self.sprite_surface.blit(self.elements["!on_button_click"][0], self.elements["!on_button_click"][1])
        elif self.is_hovered:
            self.sprite_surface.blit(self.elements["!on_button_hover"][0], self.elements["!on_button_hover"][1])
        else:
            self.sprite_surface.blit(self.elements["!on_button_normal"][0], self.elements["!on_button_normal"][1])

        destination.blit(self.sprite_surface, self.position)

    def update(self, input_data: InputData, parent_scene: Scene):
        if self.hitbox.collidepoint(input_data.mouse_pos):
            self.is_hovered = True
            input_data.add_to_cursor_queue(pg.SYSTEM_CURSOR_HAND)
        
            if input_data.mouse_pressed[0] and self.hitbox.collidepoint(input_data.click_origin):
                self.is_clicked = True
            else:
                self.is_clicked = False
        else:
            self.is_hovered = False
            self.is_clicked = False

        self.was_clicked = False
        if self.hitbox.collidepoint(input_data.mouse_pos) and not self.disabled:
            if input_data.just_released:
                if self.hitbox.collidepoint(input_data.click_origin) and self.hitbox.collidepoint(input_data.release_pos):
                    self.was_clicked = True

