#
# José Ángel Rico Mendieta -> A01707404
# Date: 03/11/2022

from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import Agent, Model
import time
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np
print("Example01.py is running...")

# Import libraries for management of data

# Import libraries for visualization

# Import libraries for time analysis

# Import libraries for simulations, with the models and agents
# Import libraries for defination of context
# Import libraries for activation of agents
# Import libraries for data collection

options = np.array([[-1, 1], [1, 0], [-1, +1], [0, -1],
                   [0, +1], [+1, -1], [+1, 0], [+1, +1]])

LIMIT = 10000


class RobotVaccumCleanerAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.pos = np.array([1, 2])

    def can_move(self, ren, col):
        return (ren >= 0 and ren < self.model.grid.height and
                col >= 0 and col < self.model.grid.width)

    def step(self):
        if self.model.floor[self.pos[0]][self.pos[1]] == 1:
            self.model.floor[self.pos[0]][self.pos[1]] = 0
        else:
            i = int(np.random.rand() * LIMIT) % len(options)
            ren = self.pos[0] + options[i][0]
            col = self.pos[1] + options[i][1]
            if self.can_move(ren, col):
                self.model.grid.move_agent(self, (ren, col))


def get_grid(model):
    grid = np.zeros((model.grid.height, model.grid.width))
    for i in range(model.grid.height):
        for j in range(model.grid.width):
            if model.grid.is_cell_empty((i, j)):
                grid[i][j] *= 2
            else:
                grid[i][j] = 1
    return grid


class RobotVacuumCleanerModel(Model):
    def __init__(self, height, width, num_robots=1, dirty_cell_percentage=0.5):
        self.num_robots = num_robots
        self.dirty_cell_percentage = dirty_cell_percentage
        self.height = height
        self.width = width
        self.grid = MultiGrid(height, width, False)
        self.floor = np.zeros((height, width))
        self.schedule = RandomActivation(self)

        amount = int(height * width * dirty_cell_percentage)
        for i in range(amount):
            finished = False
            while not finished:
                ren = int(np.random.rand() * LIMIT) % height
                col = int(np.random.rand() * LIMIT) % width
                if self.floor[ren][col] == 0:
                    self.floor[ren][col] = 1
                    finished = True

        for i in range(self.num_robots):
            a = RobotVaccumCleanerAgent(i, self)
            self.grid.place_agent(a, (0, 0))
            self.schedule.add(a)
        self.datacollector = DataCollector(
            model_reporters={"Grid": get_grid})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

    def is_all_clean(self):
        return np.all(self.floor == 0)


GRID_SIZE = 10
MAX_ITERATIONS = 200
start_time = time.time()
model = RobotVacuumCleanerModel(GRID_SIZE, GRID_SIZE)
i = 1
while not model.is_all_clean() and i <= MAX_ITERATIONS:
    model.step()
    i += 1

print("Time of execution: ", time.time() - start_time)


all_grids = model.datacollector.get_model_vars_dataframe()
fig, axs = plt.subplots(figsize=(7, 7))
axs.set_xticks([])
axs.set_yticks([])
patch = plt.imshow(all_grids.iloc[0][0], cmap="gray")

def animate(i):
    patch.set_data(all_grids.iloc[i][0])
    
anim = animation.FuncAnimation(fig, animate, frames=len(all_grids), interval=100)
anim.save('Example01.gif', writer='imagemagick', fps=10)


print("Example01.py is finished...")
