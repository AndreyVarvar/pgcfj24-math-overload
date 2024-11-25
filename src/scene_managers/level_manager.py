from tabnanny import check
from src.scene import Scene
from src.input_data import InputData
import os
import json
from src.graph import Graph
from src.constants import PALLETTE
import pygame as pg



class LevelManager():
    def __init__(self, level_dir):
        self.level_dir = level_dir
        self.current_level = 0

        self.information = {}

        self.load_next_level = True

        self.interpolate_ui = False
        self.ignore_next_ui_update = False

        self.viewing_reference = False

        self.bling_sound = pg.mixer.Sound("assets/sfx/bling.ogg")


    def update(self, input_data: InputData, parent_scene: Scene, sound_manager, dt):
        graph: Graph = parent_scene.elements["graph element"]
        check_graph: Graph = parent_scene.elements["checking graph element"]
        start_button = parent_scene.elements["start graphing button"]
        input_box = parent_scene.elements["graph input box"]
        panel = parent_scene.elements["level description"]
        next_page = parent_scene.elements["next description page button"]
        prev_page = parent_scene.elements["previous description page button"]
        hint_button = parent_scene.elements["hint button"]
        unread_page_notifier = parent_scene.elements["unread page notifier"]
        view_reference_button = parent_scene.elements["view reference button"]
        reference_text = parent_scene.elements["reference text"]

        # load next level
        if self.load_next_level:
            self.load_next_level = False
            self.current_level += 1
            self.information = self.load_level(self.current_level, check_graph, parent_scene)
            self.bling_sound.play()

        # update the unread pages notification
        if self.information["pages_read"] < (len(self.information["description"])-1) and not self.ignore_next_ui_update and not self.viewing_reference:
            unread_page_notifier.toggle_visibility(True)
        else: 
            unread_page_notifier.toggle_visibility(False)

        # update the description panel
        panel.update_text(self.information["description"][self.information["current_description_page"]])

        prev_page.disabled = (self.information["current_description_page"] == 0)
        next_page.disabled = (self.information["current_description_page"] == (len(self.information["description"])-1))

        if next_page.was_clicked:
            self.information["current_description_page"] += 1

            self.information["pages_read"] = max(self.information["pages_read"], self.information["current_description_page"])
        elif prev_page.was_clicked:
            self.information["current_description_page"] -= 1

        # update interpolation stuff
        if input_data.key_pressed == 27 and not self.interpolate_ui:  # 27 - escape key
            input_data.reset_key_event()
            self.interpolate_ui = True
            self.ignore_next_ui_update = not self.ignore_next_ui_update

        if self.interpolate_ui:
            interpolating = []
            for element in parent_scene.elements:
                if parent_scene.elements[element] in [input_box, panel, next_page, prev_page, hint_button]:
                    interpolating.append(parent_scene.elements[element].interpolate(dt))
                    
            self.interpolate_ui = any(interpolating)

        # update the graph
        if (start_button.was_clicked or input_data.key_pressed == 13) and not self.interpolate_ui:  # 13 - enter key
            input_data.reset_key_event()

            # graph.valid, formula = graph.import_new_formula(input_box.text.text)
            valid = graph.update_formula(input_box.text.text)

            if not self.ignore_next_ui_update:
                graph.start_graphing()

            if valid:
                self.ignore_next_ui_update = not self.ignore_next_ui_update
                self.interpolate_ui = True
                
        # check if the hint button was pressed
        if hint_button.was_clicked:
            if self.information["hints_used"] < len(self.information["hints"]) and (self.information["pages_read"] == (len(self.information["description"])-1)):
                self.information["hints_used"] += 1

                for hint in self.information["hints"][self.information["hints_used"] - 1]:
                    self.information["description"].append(hint)
        
        # check if the requirement was completed:
        if graph.graphing is False and len(graph.points) > 0 and len(check_graph.points) > 0 and check_graph.graphing is False:
            if self.information["requirement"]["type"] == "exact":
                if len(check_graph.points - graph.points) == 0 and len(graph.points - check_graph.points) < len(graph.points)/3:
                    self.load_next_level = True
                    check_graph.clear_points()

        # check if the reference button was pressed
        if view_reference_button.was_clicked:
            graph.toggle_visibility()
            check_graph.toggle_visibility()
            start_button.toggle_visibility()
            input_box.toggle_visibility()
            panel.toggle_visibility()
            next_page.toggle_visibility()
            prev_page.toggle_visibility()
            hint_button.toggle_visibility()
            reference_text.toggle_visibility()
            self.viewing_reference = not self.viewing_reference
            
        # DEBUGGING TOOL
        # if start_button.is_clicked:
        #     self.information = self.load_level(self.current_level, check_graph, parent_scene)
            

    def render(self, destination, dt):
        pass

    def load_level(self, n, check_graph: Graph, parent_scene: Scene):
        if parent_scene.carry_info["difficulty"] == "hard":
            if n == 11:
                parent_scene.change_scenes("main menu", {})
                n = 1
            path = os.path.join(self.level_dir, f"h{n}.json")
        else:
            if n == 18:
                parent_scene.change_scenes("main menu", {})
                n = 1
            path = os.path.join(self.level_dir, f"{n}.json")

        with open(path, 'r') as file:
            level_data = json.load(file)
        
        information = {}

        information["description"] = level_data["description"]
        information["current_description_page"] = 0
        information["pages_read"] = 0

        information["hints"] = level_data["hints"]
        information["hints_used"] = 0

        information["requirement"] = level_data["requirement"]


        if information["requirement"]["type"] == "exact":
            check_graph.update_formula(information["requirement"]["expect"])
            check_graph.start_graphing()

        return information
