import pygame as pg
from src.input_data import InputData
from src.scene import Scene
from src.utils import bound
from src.constants import *
from math import *


class Graph():
    def __init__(self):
        self.points = [set(), set()]  # second set for the points of the solution
        self.calculate_solution_graph = True
        self.formula = ["", "y=x"]

        self.interpolate = False
        self.ignore_update_to_remove_this_annoying_update_every_time = False

        self.update_graph = False
        self.graphing_progress = 128

        self.channel = pg.mixer.Channel(0)
        self.graphin = pg.mixer.Sound("assets/sfx/graphin.ogg")

        self.error_message = ""

        self.total_drawing_progress = 128
        self.x_drawing_progress = self.total_drawing_progress//2
        self.y_drawing_progress = self.total_drawing_progress

        self.graph_width = 64

        self.working_formula = ["", ""]
    
    def update(self, input_data: InputData, parent_scene: Scene, dt):
        if self.update_graph:
            self.update_graph = False
            self.graphing_progress = 0
            print(self.formula)
            for i in range(1+self.calculate_solution_graph):
                self.working_formula[i] = self._process_formula(self.formula[i])  # here i use the function to just bring everything to the left hand side

        if self.graphing_progress == self.total_drawing_progress and len(self.points[1]) > 0:
            self.calculate_solution_graph = False
    


        try:
            if self.graphing_progress < self.total_drawing_progress:
                if self.channel.get_busy() is False:
                    self.channel.play(self.graphin)

                if self.graphing_progress < self.x_drawing_progress: # graphing_progress keeps track of what point (x or y) we are plotting right now
                    x = self.graphing_progress - 32  # here, graphing progress keeps track of what x we are checking right now

                    self.remove_points_with_specific_x(x+32)

                    for i in range(1+self.calculate_solution_graph):
                        formula = self.working_formula[i].replace('x', f"({x})")  # replaces x with whatever value we are checking right now
                        solutions = self._solve_expr(formula, 'y')

                        for solution in solutions:
                            self.points[i].add((32+x, 32-round(solution)))

                
                elif self.graphing_progress < self.y_drawing_progress:
                    y = self.graphing_progress - 64 - 32 # and here as well, graphing progress keeps track of what y we are checking right now

                    for i in range(1+self.calculate_solution_graph):
                        formula = self.working_formula[i].replace('y', f"({y})")  # replaces y with whatever value we are checking right now
                        solutions = self._solve_expr(formula, 'x')

                        for solution in solutions:
                            self.points[i].add((32+round(solution), 32-y))
                                
                self.graphing_progress += 1
        except Exception as e:
            print("Congrats! you found a new unknown error:", e, " | ", self.formula)
            self.graphing_progress += 1
    

    
    def _solve_expr(self, expr, unknown):
        """solves an expression (finds all solutions it can)

        Args:
            expr (str): formula DUH, how do you think I calculate the value on the graph, huh?
            unknown (str): what value do we want to find (wether 'x' of 'y')
        Returns:
            list: solutons
        """

        solutions = []

        val = -32

        while val < 32:
            expr1 = expr.replace(unknown, f"({val})")

            # we try to find the unknown by continuesly substituting numbers and checking if the expression is equal to 0
            # i use eval, because it is very fast, and there is no point in trying to be safe here, since this will be rin on itch and all the user can do, is... hack themselves ig
            result = bound(-33, 33, eval(expr1))

            if abs(result) < 0.5:
                solutions.append(val)
            
            val += 0.1
        return solutions

    def _process_formula(self, formula) -> str:  
        try:     
            lhs, rhs = formula.split('=')   # 'rhs' - right hand side, 'lhs' - left hand side
            formula = lhs + "-(" + rhs + ")"
        except:
            formula = "2"

        return formula

    def render(self, destination: pg.Surface, dt):
        # draw cells
        for x in range(0, 64, 4):
            pg.draw.line(destination, PALLETTE["light-brown"], (x, 0), (x, 64))

        for y in range(0, 64, 4):
            pg.draw.line(destination, PALLETTE["light-brown"], (0, y), (64, y))

        # draw axis
        pg.draw.line(destination, PALLETTE["brown"], (32, 0), (32, 64))
        pg.draw.line(destination, PALLETTE["brown"], (0, 32), (64, 32))

        # draw points
        for i in range(2):
            for point in self.points[i]:
                destination.set_at(point, PALLETTE[["black", "dark-gray"][i]])

        # draw current graphing progress
        if self.graphing_progress < self.total_drawing_progress:
            if self.graphing_progress < self.x_drawing_progress:
                line_progress = self.graphing_progress / (self.total_drawing_progress / (2*self.graph_width))
                pg.draw.line(destination, PALLETTE["gray"], (line_progress, 0), (line_progress, 64))
            elif self.graphing_progress < self.y_drawing_progress:
                line_progress = 128 - (self.graphing_progress) / ((self.total_drawing_progress) // (2*self.graph_width))
                pg.draw.line(destination, PALLETTE["gray"], (0, line_progress), (64, line_progress))
    
    def remove_points_with_specific_x(self, x):
        points_to_remove = [set(), set()]
        for i in range(1+self.calculate_solution_graph):
            for p in self.points[i]:
                if p[0] == x:
                    points_to_remove[i].add(p)
        for i in range(1+self.calculate_solution_graph):
            self.points[i] = self.points[i] - points_to_remove[i]
    
    def import_new_formula(self, formula: str):
        # check validity
        valid = True
        if len(formula.split("=")) != 2:
            return False, formula
        
        lhs, rhs = formula.split("=")

        if len(rhs) == 0 or len(lhs) == 0:
            valid = False

        # insert '*' where there is implied multiplication
        lhs = self._insert_in_implied_multiplication(lhs)
        rhs = self._insert_in_implied_multiplication(rhs)

        for i in range(len(rhs)-1, 0, -1):
            if rhs[i-1] == ")" and rhs[i] == "(":
                rhs = rhs[i:] + "*" + rhs[:i]

        
        formula = lhs + "=" + rhs

        # replace '^' with '**'
        formula = formula.replace('^', '**')

        return valid, formula

    def _insert_in_implied_multiplication(self, side):
        for c in 'xy':
            side = side.split(c)
            for i, s in enumerate(side):
                if s and (s[-1].isdigit() or s[-1] == ')') and i != (len(side)-1):
                    side[i] += '*'
                elif s and s[0] == '(' and i != 0:
                    side[i] = "*" + side[i]
            
            side = c.join(side)
            
        return side
    