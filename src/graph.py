from csv import Error
import pygame as pg
from src.input_data import InputData
from src.scene import Scene
import sympy


class Graph():
    def __init__(self):
        self.points = []
        self.formula = "x = 0"
    
    def update(self, input_data: InputData, graph_scene: Scene):
        # self.formula = graph_scene.elements["text input"]
        self.points.clear()

        # try:
        for x in range(-32, 32):
                formula = self._process_formula(x, to_swap='x')

                solutions = sympy.solve(formula)

                # print(solutions, formula)

                for solution in solutions:
                    try:
                        self.points.append((x, float(solution.evalf())))  # add points to the graph
                    except TypeError:
                        pass  # the solution was complex, so 'float' coould not convert it
            
        for y in range(-32, 32):
                formula = self._process_formula(y, to_swap='y')

                solutions = sympy.solve(formula)

                # print(solutions, formula, y)

                for solution in solutions:
                    try:
                        self.points.append((float(solution.evalf()), y))  # add points to the graph
                    except TypeError:
                        pass

        # except Exception as e:
        #     print(e)
    

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
            destination.set_at((32+round(point[0]), round(32-point[1])), (255, 50, 2))