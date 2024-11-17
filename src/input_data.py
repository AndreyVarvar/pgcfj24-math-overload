import pygame as pg
from sympy import true


class InputData():
    def __init__(self):
        # A data holding class to keep all the data in one place.
        self.mouse_pos: tuple[int, int]
        self.click_origin: tuple[int, int]
        self.release_pos: tuple[int, int]
        self.mouse_pressed: tuple[bool, bool, bool]

        self.just_pressed = False
        self.just_released = False

        self.cursor_queue = []

        self.key_just_pressed = False
        self.key_pressed = None
        self.key_unicode_pressed = None


    def update(self, events):
        if len(self.cursor_queue) > 0:
            pg.mouse.set_cursor(self.cursor_queue[0])  # first item has priority
            self.cursor_queue.clear()
        else:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        self.mouse_pos = pg.Vector2(pg.mouse.get_pos())//10  # account for scaled display
        self.mouse_pressed = pg.mouse.get_pressed()

        self.just_pressed = False
        self.just_released = False
        self.key_just_pressed = False

        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.click_origin = pg.Vector2(event.pos)//10
                self.just_pressed = True
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.release_pos = pg.Vector2(event.pos)//10
                self.just_released = True

            elif event.type == pg.KEYDOWN:
                self.key_just_pressed = True
                self.key_pressed = event.key
                self.key_unicode_pressed = event.unicode
    
    def add_to_cursor_queue(self, cursor):
        if cursor not in [pg.SYSTEM_CURSOR_ARROW, pg.SYSTEM_CURSOR_CROSSHAIR, pg.SYSTEM_CURSOR_HAND, pg.SYSTEM_CURSOR_IBEAM, pg.SYSTEM_CURSOR_NO, pg.SYSTEM_CURSOR_SIZEALL, pg.SYSTEM_CURSOR_SIZENESW, pg.SYSTEM_CURSOR_SIZENS, pg.SYSTEM_CURSOR_SIZENWSE, pg.SYSTEM_CURSOR_SIZEWE, pg.SYSTEM_CURSOR_WAIT, pg.SYSTEM_CURSOR_WAITARROW]:
            print("Invalid cursor selection: ", cursor)
        else:
            self.cursor_queue.insert(0, cursor)
    
    def reset_mouse_event(self):
        self.just_pressed = False
        self.just_released = False

    def reset_key_event(self):
        self.key_just_pressed = False
        self.key_pressed = None
        self.key_unicode_pressed = None
