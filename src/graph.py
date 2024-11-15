import pygame as pg
from src.input_data import InputData
from src.scene import Scene
import sympy
from src.utils import bound


class Graph():
    def __init__(self):
        self.points = []
        self.formula = "y = x "

        self.update_graph = False
        self.graphing_progress = 0

        self.error_message = ""

        self.total_drawing_progress = 256
        self.x_drawing_progress = self.total_drawing_progress//2
        self.y_drawing_progress = self.total_drawing_progress

        self.graph_width = 64
    
    def update(self, input_data: InputData, graph_scene: Scene):
        # self.formula = graph_scene.elements["text input"]
        if self.update_graph:
            self.update_graph = False
            self.points.clear()
            self.graphing_progress = 0

        try:
            if self.graphing_progress < self.total_drawing_progress:
                if self.graphing_progress < self.x_drawing_progress:
                    x = self.graphing_progress/2 - 32

                    formula = self._process_formula(x, to_swap='x')

                    solutions = sympy.solve(formula, 'y')

                    for solution in solutions:
                        try:
                            self.points.append((x, (bound(-65, 65, float(solution.evalf())))))  # add points to the graph
                        except TypeError:
                            pass  # the solution was complex, so 'float' coould not convert it
                
                elif self.graphing_progress < self.y_drawing_progress:
                        y = self.graphing_progress/2 - 64 - 32

                        formula = self._process_formula(y, to_swap='y')

                        solutions = sympy.solve(formula, 'x')

                        for solution in solutions:
                            try:
                                self.points.append((bound(-65, 65, float(solution.evalf())), y))  # add points to the graph
                            except TypeError:
                                pass
                                
                self.graphing_progress += 1

        except NotImplementedError:
            self.graphing_progress = 128
            self.error_message = "NotImplementedError"
        except ValueError:
            self.graphing_progress += 1
    

    def _process_formula(self, val: int, to_swap: str):  # process the formula expression for SymPy to evaluate
        formula = self.formula
        if to_swap == "x":
            formula = formula.replace('x', "("+str(val)+")")
            lhs, rhs = formula.split('=')   # 'rhs' - right hand side, 'lhs' - left hand side
            formula = lhs + "-(" + rhs + ")"
        elif to_swap == "y":
            formula = formula.replace('y', "("+str(val)+")")
            lhs, rhs = formula.split('=')
            formula = lhs + "-(" + rhs + ")"
        else:
            raise Exception("what?")

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