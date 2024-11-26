from src.ui_element import UIElement
from src.input_data import InputData
from src.scene import Scene
import pygame as pg


class ButtonElement(UIElement):
    def __init__(self, format_json_path, visible=True):
        super().__init__(format_json_path, visible=visible)

        self.is_clicked = False  # clicked and still holding
        self.is_hovered = False

        self.was_clicked = False  # clicked and released
        self.disabled = False  # block the mouse from being used

        self.click_sound = pg.mixer.Sound("assets/sfx/button.ogg")
    
    def render_element(self, destination, dt):
        self.sprite_surface.fill((0, 0, 0, 0))  # clear the sprite

        draw_special = True
        for element in self.sort_elements_by_layer():
            if element[0] == "!":
                element_to_draw = ["!on_button_normal", "!on_button_hover", "!on_button_click", "!on_button_disabled"][max([3*self.disabled, 2*self.is_clicked, self.is_hovered, 0])]
                if draw_special:
                    draw_special = False
                    self.sprite_surface.blit(self.information["elements"][element_to_draw][0], self.information["elements"][element_to_draw][1])

            else:
                self.sprite_surface.blit(self.information["elements"][element][0], self.information["elements"][element][1])

        destination.blit(self.sprite_surface, self.information["uielement"]["position"])

    def update_element(self, input_data: InputData, parent_scene: Scene, sound_manager, dt):
        if self.get_hitbox().collidepoint(input_data.mouse_pos) and not self.disabled:
            self.is_hovered = True
            input_data.add_to_cursor_queue(pg.SYSTEM_CURSOR_HAND)
        
            if input_data.mouse_pressed[0] and self.get_hitbox().collidepoint(input_data.click_origin):
                self.is_clicked = True

                input_data.reset_mouse_event()
            else:
                self.is_clicked = False
        else:
            self.is_hovered = False
            self.is_clicked = False

        self.was_clicked = False
        if self.get_hitbox().collidepoint(input_data.mouse_pos) and not self.disabled:
            if input_data.just_released:
                if self.get_hitbox().collidepoint(input_data.click_origin) and self.get_hitbox().collidepoint(input_data.release_pos):
                    self.was_clicked = True
                    self.click_sound.play()

