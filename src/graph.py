import pygame as pg
from src.input_data import InputData
from src.scene import Scene
import sympy
from src.utils import bound
from src.constants import *


class Graph():
    def __init__(self):
        self.points = set()
        self.formula = "y = cos(x)"

        self.interpolate = False
        self.ignore_update_to_remove_this_annoying_update_every_time = False

        self.update_graph = False
        self.graphing_progress = 128

        self.error_message = ""

        self.total_drawing_progress = 128
        self.x_drawing_progress = self.total_drawing_progress//2
        self.y_drawing_progress = self.total_drawing_progress

        self.graph_width = 64
    
    def update(self, input_data: InputData, parent_scene: Scene, dt):
        # self.formula = graph_scene.elements["text input"]
        if self.update_graph:
            self.update_graph = False
            self.graphing_progress = 0
            self.formula: str = self._process_formula('x', to_swap='x')  # here i use the function to just bring everything to the left hand side
            try:
                self.formula = sympy.parsing.sympy_parser.parse_expr(self.formula)
            except Exception as e:
                print("Error parsing formula: ", e)
                self.graphing_progress = 128

        try:
            if self.graphing_progress < self.total_drawing_progress:
                if self.graphing_progress < self.x_drawing_progress: # graphing_progress keeps track of what point (x or y) we are plotting right now
                    x = self.graphing_progress - 32  # here, graphing progress keeps track of what x we are checking right now

                    self.remove_points_with_specific_x(x+32)

                    formula = self.formula.subs('x', x)  # replaces x with whatever value we are checking right now
                    solutions = self._solve_expr(formula, 'y')

                    for solution in solutions:
                        self.points.add((32+x, 32-round(solution)))

                
                elif self.graphing_progress < self.y_drawing_progress:
                    y = self.graphing_progress - 64 - 32 # and here as well, graphing progress keeps track of what y we are checking right now

                    formula = self.formula.subs('y', y)  # replaces y with whatever value we are checking right now
                    solutions = self._solve_expr(formula, 'x')

                    for solution in solutions:
                        self.points.add((32+round(solution), 32-y))
                                
                self.graphing_progress += 1

        except ValueError as e:
            self.graphing_progress += 1
            print(e)
        except TypeError as e:
            self.graphing_progress += 1
            self.error_message = "Something went wrong"
            print("Computational error of '", formula, "': ", e)
    

    
    def _solve_expr(self, expr, unknown):
        """solves an expression (finds all solutions it can)

        Args:
            expr (sympy expression): sympy expression
            unknown (str): what value do we want to find (wither 'x' of 'y')
        Returns:
            list: solutons
        """

        solutions = []

        val = -32
        prev_val = -33

        while val < 32:
            expr1 = expr.subs(unknown, val)
            if expr1.has(sympy.I) or expr1.has(sympy.zoo):  # make sure there are no complex parts (we are working in the real plane DUH)
                return []

            # we try to find the unknown by continuesly substituting numbers and checking if the expression is equal to 0 (since that's how sympy solver works)
            result = bound(-33, 33, expr1.evalf())

            if abs(result) < 0.9:
                solutions.append(val)

            rate_of_change = (expr1 - expr.subs(unknown, prev_val)).evalf()/(val-prev_val)  # rough differential definition. Math is useful! (i mean, this is a game where math is needed, so who am i kidding)
            step = 1 if ((rate_of_change == 0) or (abs(result) > 32)) else (1/abs(rate_of_change))
            
            prev_val = val
            val += max(min(step, 1), 0.5)
        return solutions

    def _process_formula(self, val, to_swap: str) -> str:  # process the formula expression for SymPy to evaluate
        formula = self.formula
        
        formula = formula.replace(to_swap, "("+str(val)+")")
        lhs, rhs = formula.split('=')   # 'rhs' - right hand side, 'lhs' - left hand side
        formula = lhs + "-(" + rhs + ")"

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
        for point in self.points:
            destination.set_at(point, PALLETTE["black"])

        # draw current graphing progress
        if self.graphing_progress < self.total_drawing_progress:
            if self.graphing_progress < self.x_drawing_progress:
                line_progress = self.graphing_progress / (self.total_drawing_progress / (2*self.graph_width))
                pg.draw.line(destination, PALLETTE["gray"], (line_progress, 0), (line_progress, 64))
            elif self.graphing_progress < self.y_drawing_progress:
                line_progress = 128 - (self.graphing_progress) / ((self.total_drawing_progress) // (2*self.graph_width))
                pg.draw.line(destination, PALLETTE["gray"], (0, line_progress), (64, line_progress))
    
    def remove_points_with_specific_x(self, x):
        points_to_remove = set()
        for p in self.points:
            if p[0] == x:
                points_to_remove.add(p)
        
        self.points = self.points - points_to_remove
    
    def import_new_formula(self, formula: str):
        # check validity
        valid = True
        if "=" not in formula:
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

        # replace all lowercase 'e' with eulers constant
        formula = formula.replace('e', 'E')
        for i in range(1, len(formula)-2):
            if formula[i] == "E" and formula[i-1] in "sc":
                formula = formula[:i] + formula[i].lower() + formula[i+1:]
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
    