from src.scene import Scene
from src.input_data import InputData
from src.graph import Graph
from src.utils import Timer
from random import choice



class MainMenuManager():
    def __init__(self):
        self.timer = Timer([5], True)
        self.formulas = ["SPECIAL FUNCTION", "y=x", "y=abs(x)", "y=0.1x^2", "y=10*sin(x/10)"]


    def update(self, input_data: InputData, parent_scene: Scene, sound_manager, dt):
        graph: Graph = parent_scene.elements["background element"]
        quit_button = parent_scene.elements["quit button"]
        play_button = parent_scene.elements["play button"]

        if self.timer.tick(dt):
            graph.update_formula(choice(self.formulas))
            graph.start_graphing()

        if quit_button.was_clicked:
            parent_scene.quit = True

        if play_button.was_clicked:
            parent_scene.change_scenes("game")


    def render(self, destination, dt):
        pass
