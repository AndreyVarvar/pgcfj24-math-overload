from tabnanny import check
from src.scene import Scene
from src.input_data import InputData
import os
import json
from src.graph import Graph



class LevelManager():
    def __init__(self, level_dir):
        self.level_dir = level_dir
        self.current_level = 0

        self.information = {}

        self.load_next_level = True

        self.interpolate_ui = False
        self.ignore_next_ui_update = False


    def update(self, input_data: InputData, parent_scene: Scene, dt):
        graph: Graph = parent_scene.elements["graph element"]
        check_graph: Graph = parent_scene.elements["checking graph element"]
        start_button = parent_scene.elements["start graphing button"]
        input_box = parent_scene.elements["graph input box"]
        panel = parent_scene.elements["level description"]
        next_page = parent_scene.elements["next description page button"]
        prev_page = parent_scene.elements["previous description page button"]
        hint_button = parent_scene.elements["hint button"]
        unread_page_notifier = parent_scene.elements["unread page notifier"]

        # load next level
        if self.load_next_level:
            self.load_next_level = False
            self.current_level += 1
            self.information = self.load_level(self.current_level, check_graph)

        # update the unread pages notification
        if self.information["pages_read"] < (len(self.information["description"])-1) and not self.ignore_next_ui_update:
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
            if self.information["hints_used"] < len(self.information["hints"]):
                self.information["hints_used"] += 1

                for hint in self.information["hints"][self.information["hints_used"] - 1]:
                    self.information["description"].append(hint)
        
        # check if the requirement was completed:
        if graph.graphing is False and len(graph.points) > 0 and len(check_graph.points) > 0 and check_graph.graphing is False:
            if self.information["requirement"]["type"] == "exact":
                # print(graph.points.difference(graph.points))
                if len(check_graph.points - graph.points) == 0:
                    self.load_next_level = True
                    check_graph.clear_points()
            
        # DEBUGGING TOOL
        # if start_button.is_clicked:
        #     self.information = self.load_level(self.current_level, check_graph)
        #     if self.information["requirement"]["type"] == "exact":
        #         graph.formula[1] = graph.import_new_formula(self.information["requirement"]["expect"])[1]
        #         graph.points[1].clear()
            

    def render(self, destination, dt):
        pass

    def load_level(self, n, check_graph: Graph):
        try:
            with open(os.path.join(self.level_dir, f"{n}.json"), 'r') as file:
                level_data = json.load(file)
        except:
            return self.information
        
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
