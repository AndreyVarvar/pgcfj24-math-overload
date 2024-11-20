from math import sin, pi
import pygame as pg


def bound(low: int, high: int, i: int):
    return min(max(i, low), high)


class Timer():
    def __init__(self, 
                 periods: list[int],
                 loop: bool):
        self.periods = periods

        if len(periods) == 0:
            raise Exception("Timer must have at least 1 period")

        self.loop = loop

        self.time = 0
        self.current_period = 0

        self.percent = 0

    def tick(self, dt):
        self.time += dt
        self.percent = self.time / self.periods[self.current_period]
        
        changed = False

        while self.current_period < len(self.periods) and self.time > self.periods[self.current_period]:
            changed = True
            self.time -= self.periods[self.current_period]
            self.current_period += 1
            if self.current_period >= len(self.periods) and self.loop:
                self.current_period = 0
        
        return changed

    def reset(self):
        self.current_period = 0
        self.time = 0


def interpolate(object, dt):
    next_index = object.information["info"]["current_interpolation"] + 1
    if next_index >= len(object.information["info"]["interpolation_points"]):
        next_index = 0

    dist = object.information["info"]["interpolation_points"][next_index] - object.information["info"]["position"]

    interpolation_speed = dist.length() / object.information["info"]["interpolation_time"]

    distance_traveled = dist * interpolation_speed * dt

    # print(dist, distance_traveled, interpolation_speed, next_index, object.information["info"]["interpolation_points"][next_index])

    if distance_traveled.length() >= (dist.length()-1):
        object.information["info"]["current_interpolation"] += 1
        if object.information["info"]["current_interpolation"] >= len(object.information["info"]["interpolation_points"]):
            object.information["info"]["current_interpolation"] = 0
        object.information["info"]["position"] = object.information["info"]["interpolation_points"][object.information["info"]["current_interpolation"]].copy()
        return True
    else:
        object.information["info"]["position"] += distance_traveled
        return False
