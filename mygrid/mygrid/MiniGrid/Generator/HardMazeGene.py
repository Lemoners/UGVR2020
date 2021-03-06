from ..Discriminator.HardMazeDiscriminator import HardMazeDiscriminator
from .MazeGene import MazeGene
from .HyperPara import GRID_HEIGHT, GRID_WIDTH

import numpy as np
import bisect
import random

class HardMazeGene(object):
    """ HardMazeGene

    Generate relatively hard maze-like grids based on hand-crafted heuristic metric.
    """
    def __init__(self):
        super().__init__()
        self.discriminator = HardMazeDiscriminator()
        self.generator = MazeGene()
        self.maze_pool = []
    
    def gene(self, grid_width=GRID_WIDTH, grid_height=GRID_HEIGHT, threshold=0.01):
        """ Generate one hard grid.

        Equals to self.batch_gene(batches=1), keep this function for OOP purpose.

        :returns: grid: numpy.matrix
        :returns: start position for the agent: (0,0)
        :returns: goal position: (GRID_WIDTH-1,GRID_HEIGHT-1)
        """
        all_batches = int(1 / threshold)
        mazes = self.batch_gene(batches=1, grid_width=grid_width, grid_height=grid_height, threshold=threshold)
        return mazes[0], (0,0), (GRID_WIDTH-1, GRID_HEIGHT-1)


    def batch_gene(self, grid_width=GRID_WIDTH, grid_height=GRID_HEIGHT, batches=1, threshold=0.1):
        """ Generate `batches` of hard grids, with threshold=threshold.

        We first generate `batches / threshold` maze-like grids, then evaluate them based on hand-crafted metric.
        Finally we select the top `100*threshold` percent hard grids.
        
        :returns: mazes: [numpy.matrix]
        """
        all_batches = int(batches / threshold)
        left_for_gene = all_batches - len(self.maze_pool)

        for i in range(left_for_gene):
            maze, _, _ = self.generator.gene(grid_width=grid_width, grid_height=grid_height,)
            score, _ = self.discriminator.evaluate_maze(maze)
            pos = bisect.bisect_right([-m[1] for m in self.maze_pool], -score)
            self.maze_pool.insert(pos, (maze, score))

        mazes = [m[0] for m in self.maze_pool[:batches]]
        self.maze_pool = self.maze_pool[batches:]

        # randomly expire some grids
        self.maze_pool = self.maze_pool[:random.randint(0, len(self.maze_pool))]
        return mazes


class SimpleHardMazeGene(HardMazeGene):
    """ SimpleHardMazeGene
    Generate grids without agent and goal. (only with walls and empty cells, used for training VAE)
    """
    def gene(self):
        grid, pos, goal_pos = super().gene()
        grid[pos[1], pos[0]] = 0
        grid[goal_pos[1], goal_pos[0]] = 0
        return grid



