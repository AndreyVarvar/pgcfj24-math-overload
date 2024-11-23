import pygame as pg


class SoundManager():
    def __init__(self):
        pass
    
    def play_sound(self, sound_path, channel):
        if pg.mixer.Channel(channel).get_busy() is False:
            pg.mixer.Channel(channel).play(pg.mixer.sound(sound_path))

