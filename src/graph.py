import pygame as pg
from src.input_data import InputData
from src.scene import Scene
from src.constants import PALLETTE
import sys
import os
from math import *
    

class Graph():
    def __init__(self, render, precision):
        self.points = set()
        self.formula = ""

        self.total_graphing_progress = 128
        self.graphing_progress = self.total_graphing_progress

        self.currently_graphing = 'x'

        self.channel = pg.mixer.Channel(0)
        self.graphing_sound = pg.mixer.Sound("assets/sfx/graphin.ogg")

        self.render_self = render

        self.graph_width = 64

        self.precision = precision

        self.graphing = False
     
    def update(self, input_data: InputData, parent_scene: Scene, sound_manager, dt):
        self.graphing = self.graphing_progress < self.total_graphing_progress
        self.currently_graphing = 'yx'[self.graphing_progress < (self.total_graphing_progress//2)]

        if self.graphing:
            if self.channel.get_busy() is False and self.render_self:
                self.channel.play(self.graphing_sound)

            if self.formula == "SPECIAL FUNCTION":
                if self.graphing_progress >= self.total_graphing_progress//2:
                    self.graphing_progress = self.total_graphing_progress
                self.clear_previous_points_column(self.graphing_progress)
                points = self.special_function(self.graphing_progress)
                self.points = self.points.union(points)

            elif self.currently_graphing == 'x':
                x = self.graphing_progress - 32
                self.clear_previous_points_column(x+32)

                solutions = self.solve_expr(self.formula.replace('x', f"({x})"), solve_for='y')

                for solution in solutions:
                    self.points.add((32+x, 32-round(solution)))  # '32+x' because in the graph we are working in range of (-32, 32), but we need a range of (0, 64)

            elif self.currently_graphing == 'y':
                y = self.graphing_progress - 64 - 32 
                
                solutions = self.solve_expr(self.formula.replace('y', f"({y})"), solve_for='x')

                for solution in solutions:
                    self.points.add((32+round(solution), 32-y))
            
            self.graphing_progress += 1

    def render(self, destination: pg.Surface, dt):
        if self.render_self:
            # draw cells
            for x in range(0, 64, 4):
                pg.draw.line(destination, PALLETTE["light-brown"], (x, 0), (x, 64))

            for y in range(0, 64, 4):
                pg.draw.line(destination, PALLETTE["light-brown"], (0, y), (64, y))

            # draw axis
            pg.draw.line(destination, PALLETTE["brown"], (32, 0), (32, 64))
            pg.draw.line(destination, PALLETTE["brown"], (0, 32), (64, 32))

            # draw points
            for point in self.points:
                destination.set_at(point, PALLETTE["black"])

            # draw current graphing progress
            if self.graphing_progress < self.total_graphing_progress:
                if self.currently_graphing == 'x':
                    line_progress = self.graphing_progress / (self.total_graphing_progress / (2*self.graph_width))
                    pg.draw.line(destination, PALLETTE["gray"], (line_progress, 0), (line_progress, 64))
                elif self.currently_graphing == 'y':
                    line_progress = 128 - (self.graphing_progress) / ((self.total_graphing_progress) // (2*self.graph_width))
                    pg.draw.line(destination, PALLETTE["gray"], (0, line_progress), (64, line_progress))

    def clear_previous_points_column(self, x):
        points_to_remove = set()
        for p in self.points:
            if p[0] == x:
                points_to_remove.add(p)
        
        self.points = self.points - points_to_remove

    def solve_expr(self, formula, solve_for):
        try:
            solutions = []

            val = -32

            while val < 32:
                expr1 = formula.replace(solve_for, f"({val})")

                # we try to find the unknown by continuesly substituting numbers and checking if the expression is equal to 0
                # NOTE: this 'eval' function only evaluates the expression inputted by the player. If you still don't trust me, go play the web-version on itch
                result = eval(expr1) 

                if abs(result) < 0.5:  # tolerance, since we can't calculate the "exact" value
                    solutions.append(val)
                
                val += self.precision

            return solutions
        except Exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, self.formula)

            return []
        
    def update_formula(self, new_formula):
        valid, new_formula = self.process_new_formula(new_formula)

        if valid or new_formula == "SPECIAL FUNCTION":
            self.formula = new_formula
        else:
            self.formula = "1"

        return valid
    
    def start_graphing(self):
        self.graphing_progress = 0

    def process_new_formula(self, new_formula):
        # check validity
        valid = True
        if len(new_formula.split("=")) != 2:
            return False, new_formula
        
        lhs, rhs = new_formula.split("=")

        if len(rhs) == 0 or len(lhs) == 0:
            valid = False

        # insert '*' where there is implied multiplication
        lhs = self.insert_implied_multiplication(lhs)
        rhs = self.insert_implied_multiplication(rhs)

        
        formula = lhs + "-(" + rhs + ")"

        # replace '^' with '**'
        formula = formula.replace('^', '**')

        return valid, formula

    def insert_implied_multiplication(self, expression):
        indexes = []
        for i in range(len(expression)-1):
            if expression[i].isdigit() and (expression[i+1].isdigit() is False and expression[i+1] not in "+-=*/).,"):
                indexes.append(i+1)
        for i in indexes[::-1]:
            expression = expression[:i] + "*" + expression[i:]
        
        for i in range(len(expression)-1, 0, -1):  
            if expression[i-1] == ")" and expression[i] == "(":
                expression = expression[i:] + "*" + expression[:i]
            
        return expression
    
    def clear_points(self):
        self.points.clear()

    def toggle_visibility(self):
        self.render_self = not self.render_self

    def special_function(self, val):
        points = set()
        for x in range(pg_image.get_width()):
            for y in range(pg_image.get_height()):
                if val == x:
                    if pg_image.get_at((x, y)) != (0, 0, 0, 0):
                        points.add((x, y))
        return points

pg_image = pg.image.load("assets/sprites/pygame_function.png")
