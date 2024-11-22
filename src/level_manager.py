from src.scene import Scene
from src.input_data import InputData
import os
import json



class LevelManager():
    def __init__(self, level_dir):
        self.level_dir = level_dir
        self.current_level = 1

        self.information = self.load_level(self.current_level)


    def update(self, input_data: InputData, parent_scene: Scene, dt):
        graph = parent_scene.elements["graph element"]
        start_button = parent_scene.elements["start graphing button"]
        input_box = parent_scene.elements["graph input box"]
        panel = parent_scene.elements["level description"]
        next_page = parent_scene.elements["next description page button"]
        prev_page = parent_scene.elements["previous description page button"]
        hint_button = parent_scene.elements["hint button"]
        unread_page_notifier = parent_scene.elements["unread page notifier"]

        # update the unread pages notification
        if self.information["pages_read"] < (len(self.information["description"])-1) and not graph.ignore_update_to_remove_this_annoying_update_every_time:
            unread_page_notifier.visible = True
        else:
            unread_page_notifier.visible = False

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
        if graph.interpolate:
            interpolating = []
            for element in parent_scene.elements:
                if parent_scene.elements[element] in [input_box, panel, next_page, prev_page, hint_button]:
                    interpolating.append(parent_scene.elements[element].interpolate(dt))
                    
            graph.interpolate = any(interpolating)
        
        if input_data.key_pressed == 27 and not graph.interpolate:  # 27 - escape key
            input_data.reset_key_event()
            graph.interpolate = True
            graph.ignore_update_to_remove_this_annoying_update_every_time = not graph.ignore_update_to_remove_this_annoying_update_every_time

        # update the graph
        if (start_button.was_clicked or input_data.key_pressed == 13) and not graph.interpolate:  # 13 - enter key
            input_data.reset_key_event()

            graph.valid, formula = graph.import_new_formula(input_box.text.text)

            if graph.valid:
                graph.interpolate = True
                if not graph.ignore_update_to_remove_this_annoying_update_every_time:
                    graph.formula = formula
                    graph.update_graph = True
                    graph.ignore_update_to_remove_this_annoying_update_every_time = True
                else:
                    graph.ignore_update_to_remove_this_annoying_update_every_time = False

    def render(self, destination, dt):
        pass

    def load_level(self, n):
        with open(os.path.join(self.level_dir, f"{n}.json"), 'r') as file:
            level_data = json.load(file)
        
        information = {}

        information["description"] = level_data["description"]
        information["current_description_page"] = 0
        information["pages_read"] = 0

        return information
