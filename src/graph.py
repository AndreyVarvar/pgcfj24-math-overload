from pkg_resources import UnknownExtra
import pygame as pg
from src.input_data import InputData
from src.scene import Scene
import sympy
from src.utils import bound


class Graph():
    def __init__(self):
        self.points = []
        self.formula = "y = ln(x)"

        self.update_graph = True
        self.graphing_progress = 128

        self.error_message = ""

        self.total_drawing_progress = 128
        self.x_drawing_progress = self.total_drawing_progress//2
        self.y_drawing_progress = self.total_drawing_progress

        self.graph_width = 64
    
    def update(self, input_data: InputData, graph_scene: Scene):
        # self.formula = graph_scene.elements["text input"]
        if self.update_graph:
            self.update_graph = False
            self.points.clear()
            self.graphing_progress = 0

            self.formula: str = self._process_formula('x', to_swap='x')  # here i use the function to just bring everything to the left hand side
            self.formula = sympy.parsing.sympy_parser.parse_expr(self.formula)

            
            print(sympy.solve(self.formula, 'x'))
            self.formula_x_diff = sympy.diff(self.formula, 'x')

            # print(self.formula_x_diff)
            # print(self.formula_y_diff)


        try:
            if self.graphing_progress < self.total_drawing_progress:
                if self.graphing_progress < self.x_drawing_progress: # graphing_progress keeps track of what point (x or y) we are plotting right now
                    x = self.graphing_progress - 32  # here, graphing progress keeps track of what x we are checking right now

                    formula = self.formula.subs('x', x)  # replaces x with whatever value we are checking right now
                    solutions = self._solve_expr(formula, 'y', self.formula_x_diff, 'x', x)

                    for solution in solutions:
                        self.points.append((x, solution))

                
                elif self.graphing_progress < self.y_drawing_progress:
                    y = self.graphing_progress - 64 - 32 # and here as well, graphing progress keeps track of what y we are checking right now

                    formula = self.formula.subs('y', y)  # replaces y with whatever value we are checking right now
                    solutions = self._solve_expr(formula, 'x', self.formula_x_diff, 'x', y)

                    for solution in solutions:
                        self.points.append((solution, y))
                                
                self.graphing_progress += 1

        except ValueError as e:
            self.graphing_progress += 1
            print(e)
        except TypeError as e:
            self.graphing_progress += 1
            self.error_message = "We dont support variables"
            print("NO VARIABLES: ", e)
    
    def _solve_expr(self, expr, unknown, diff, diff_unknown, curr):
        """solves an expression (finds all solutions it can)

        Args:
            expr (sympy expression): sympy expression
            unknown (str): what value do we want to find (wither 'x' of 'y')
            diff (sympy expression): differential of the expression (we calculate it ahead of time outside the function to not waste unnecessary resourses)
            diff_unknown (str): what value do we substitute in the differential
            curr (int): for what value (either 'x' or 'y') are we currently finding solutions? For example, if 'unknow' is 'x', then 'curr' is 'y' 

        Returns:
            list: solutons
        """
        solutions = []

        val = -32

        while val < 32:
            if expr.subs(unknown, val).has(sympy.I) or expr.subs(unknown, val).has(sympy.zoo):  # make sure there are no complex parts (we are working in the real plane DUH)
                return []

            # we try to find the unknown by continuesly substituting numbers and checking if the expression is equal to 0 (since that's how sympy solver works)
            result = bound(-33, 33, expr.subs(unknown, val).evalf())
            # if abs(result) < 33:
            #     print(expr, val, result)
            if abs(result) < 0.9:
                solutions.append(val)
            
            rate_of_change = abs(diff.subs(diff_unknown, curr).evalf())
            step = 1 if ((rate_of_change == 0) or (abs(result) > 32)) else (5/rate_of_change)

            # print(expr, val, rate_of_change)


            
            val += max(min(step, 1), 0.1)
        return solutions

    def _process_formula(self, val, to_swap: str) -> str:  # process the formula expression for SymPy to evaluate
        formula = self.formula
            
        formula = formula.replace(to_swap, "("+str(val)+")")
        lhs, rhs = formula.split('=')   # 'rhs' - right hand side, 'lhs' - left hand side
        formula = lhs + "-(" + rhs + ")"

        return formula

    def render(self, destination: pg.Surface):
        # draw cells
        for x in range(0, 64, 4):
            pg.draw.line(destination, (205, 203, 209), (x, 0), (x, 64))

        for y in range(0, 64, 4):
            pg.draw.line(destination, (205, 203, 209), (0, y), (64, y))
        # draw axis
        pg.draw.line(destination, (132, 129, 138), (32, 0), (32, 64))
        pg.draw.line(destination, (132, 129, 138), (0, 32), (64, 32))

        # draw points
        for point in self.points:
            destination.set_at((32+round(point[0]), 32-round(point[1])), (255, 50, 2))

        # draw current graphing progress
        if self.graphing_progress < self.total_drawing_progress:
            if self.graphing_progress < self.x_drawing_progress:
                line_progress = self.graphing_progress / (self.total_drawing_progress / (2*self.graph_width))
                pg.draw.line(destination, (66, 135, 245), (line_progress, 0), (line_progress, 64))
            elif self.graphing_progress < self.y_drawing_progress:
                line_progress = 128 - (self.graphing_progress) / ((self.total_drawing_progress) // (2*self.graph_width))
                pg.draw.line(destination, (66, 135, 245), (0, line_progress), (64, line_progress))