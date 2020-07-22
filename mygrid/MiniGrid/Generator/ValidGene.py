from .HyperPara import *
import numpy as np
from ..Utils.BFS import BFSAgent


class ValidGene(object):
    def __init__(self):
        super().__init__()
        self.bfs = BFSAgent()

    def gene(self):
        """
        Describe: generate solvable maze
        return: grid: numpy.matrix
        return: pos: (x,y)
        return: goal_pos: (x,y)
        """
        while True:
            grid = np.random.randint(0, 2, (GRID_HEIGHT, GRID_WIDTH))
            grid[0, 0] = AGENT
            grid[GRID_HEIGHT - 1, GRID_WIDTH - 1] = GOAL
            h, solvable = self.bfs.solve(grid)
            if solvable:
                break
        return grid, (0, 0), (GRID_WIDTH-1, GRID_HEIGHT-1)

    def update(self, data):
        pass
