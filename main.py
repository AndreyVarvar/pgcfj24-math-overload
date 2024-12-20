import pygame as pg

from src.scene_managers.main_menu_manager import MainMenuManager
from src.input_data import InputData
from src.scene import Scene
from src.graph import Graph
from src.font import Font
from src.constants import PALLETTE

from src.scene_managers.level_manager import LevelManager
from src.sound_manager import SoundManager

from src.UI.button import ButtonElement
from src.UI.input_box import InputBoxElement
from src.UI.panel import Panel
from src.UI.text import TextElement

import asyncio

pg.init()


class Game():
    def __init__(self):
        self.window = pg.display.set_mode([640, 640])
        self.screen = pg.Surface((64, 64), pg.SRCALPHA)

        self.input_data = InputData()

        self.running = True

        self.clock = pg.time.Clock()
        self.FPS = 64*64

        self.font = Font("assets/formatting/mathematica_font.json")

        pg.mixer.music.set_volume(0.0)
        self.sound_manager = SoundManager()

        self.scenes = {
            "game": Scene({
                "level manager": LevelManager("assets/levels", 17),
                "graph element": Graph(True, 0.1),
                "checking graph element": Graph(False, 0.1),
                "mouse x pos": TextElement((50, 50), "x ", self.font, False, visible=False, shadow=True),
                "mouse y pos": TextElement((50, 50), "y ", self.font, False, visible=False, shadow=True),
                "start graphing button": ButtonElement("assets/formatting/game/start_graphing_button.json"),
                "view reference button": ButtonElement("assets/formatting/game/view_reference_button.json"),
                "graph input box": InputBoxElement("assets/formatting/game/formula_input_box.json", self.font),
                "level description": Panel("assets/formatting/game/description_panel.json", self.font),
                "next description page button": ButtonElement("assets/formatting/game/next_page_button.json"),
                "previous description page button": ButtonElement("assets/formatting/game/previous_page_button.json"),
                "to main menu button": ButtonElement("assets/formatting/game/to_main_menu_button.json", visible=False),
                "next level button": ButtonElement("assets/formatting/game/next_level_button.json"),
                "hint button": ButtonElement("assets/formatting/game/hint_button.json"),
                "unread page notifier": TextElement((50, 40), "&", self.font, True),
                "reference text": TextElement((2, 1), "reference graph", self.font, shadow=True, visible=False)
            }, "assets/music/game.wav"),
            "hard game": Scene({
                "level manager": LevelManager("assets/hard_levels", 11),
                "graph element": Graph(True, 0.1),
                "checking graph element": Graph(False, 0.1),
                "mouse x pos": TextElement((50, 50), "x ", self.font, False, visible=False, shadow=True),
                "mouse y pos": TextElement((50, 50), "y ", self.font, False, visible=False, shadow=True),
                "start graphing button": ButtonElement("assets/formatting/game/start_graphing_button.json"),
                "view reference button": ButtonElement("assets/formatting/game/view_reference_button.json"),
                "graph input box": InputBoxElement("assets/formatting/game/formula_input_box.json", self.font),
                "level description": Panel("assets/formatting/game/description_panel.json", self.font),
                "next description page button": ButtonElement("assets/formatting/game/next_page_button.json"),
                "previous description page button": ButtonElement("assets/formatting/game/previous_page_button.json"),
                "to main menu button": ButtonElement("assets/formatting/game/to_main_menu_button.json", visible=False),
                "next level button": ButtonElement("assets/formatting/game/next_level_button.json"),
                "hint button": ButtonElement("assets/formatting/game/hint_button.json"),
                "unread page notifier": TextElement((50, 40), "&", self.font, True),
                "reference text": TextElement((2, 1), "reference graph", self.font, shadow=True, visible=False)
            }, "assets/music/game.wav"),
            "main menu": Scene({
                "background element": Graph(True, 0.5),
                "play button": ButtonElement("assets/formatting/main_menu/play_button.json"),
                "hard button": ButtonElement("assets/formatting/main_menu/hard_button.json"),
                "quit button": ButtonElement("assets/formatting/main_menu/quit_button.json"),
                "manager": MainMenuManager()
            }, "assets/music/main-menu.wav")
        }

        self.current_scene = self.scenes["main menu"]

    
    async def run(self):
        while self.running:
            dt = self.clock.tick(self.FPS)/1000 + 0.001  # to avoid 'division by 0' error

            pg.display.set_caption(str(round(1/dt)))

            self.handle_events()
            self.update(dt)
            self.render(dt)

            await asyncio.sleep(0)

        pg.quit()

    def render(self, dt):
        self.window.fill(PALLETTE["white"])
        self.screen.fill(PALLETTE["white"])

        for element in self.current_scene.elements:
            self.current_scene.elements[element].render(self.screen, dt)


        self.window.blit(pg.transform.scale_by(self.screen, 10), (0, 0))

        pg.display.update()
    
    def update(self, dt):
        self.current_scene.update(self.input_data, self.sound_manager, dt)

        if self.current_scene.quit is True:
            self.running = False

        if self.current_scene.change_scene is True:
            new_scene_name = self.current_scene.new_scene_name

            self.current_scene.reset_scene_change()
            self.current_scene = self.scenes[new_scene_name]

            self.input_data.just_changed_scenes = True

    def handle_events(self):
        events = pg.event.get()
        self.input_data.update(events)

        for event in events:
            if event.type == pg.QUIT:
                self.running = False

asyncio.run(Game().run())

