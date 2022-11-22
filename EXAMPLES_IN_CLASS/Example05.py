import datetime
import time
import pandas as pd
import numpy as np
from mesa import Agent, Model

from mesa.space import SingleGrid

from mesa.time import RandomActivation

from mesa.datacollection import DataCollector

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.rcParams["animation.html"] = "jshtml"
matplotlib.rcParams['animation.embed_limit'] = 2**128


class SegregationAgent(Agent):
    def __init__(self, unique_id, model, a_type, threshold):
        super().__init__(unique_id, model)
        self.type = a_type
        self.threshold = threshold

    def step(self):
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore=True, include_center=False)
        same_type = 0
        total_neighbors = 0
        fraction = 0
        for neighbour in neighbors:
            if self.type == neighbour.type:
                same_type += 1
            total_neighbors += 1
        if total_neighbors != 0:
            fraction = same_type / total_neighbors

        if fraction < self.threshold:
            self.model.grid.move_to_empty(self)


def get_grid(model):
    grid = np.zeros((model.grid.width, model.grid.height))
    for (content, x, y) in model.grid.coord_iter():
        if (content == None):
            grid[x][y] = 0
        else:
            grid[x][y] = content.type
    return grid


class SegregationModel(Model):
    def __init__(self, width, heigth, diff_types=2, threshlod=0.30, empty_cells=0.20):
        self.num_agents = width * heigth * (1-empty_cells)
        self.grid = SingleGrid(width, heigth, False)
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(model_reporters={"Grid": get_grid})

        id = 0
        amount = int(self.num_agents / diff_types)
        for my_type in range(1, diff_types+1):
            for j in range(amount):
                a = SegregationAgent(id, self, my_type, threshlod)
                (x, y) = self.grid.find_empty()
                self.grid.place_agent(a, (x, y))
                self.schedule.add(a)
                id += 1

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()


WIDTH = 30
HEIGHT = 30
THRESHOLD = 0.60
TYPES = 2
EMPTY_CELLS = 0.20
MAX_ITERATIONS = 100

start_time = time.time()
model = SegregationModel(WIDTH, HEIGHT, TYPES, THRESHOLD, EMPTY_CELLS)

for i in range(MAX_ITERATIONS):
    model.step()

print("Execution time: %s seconds" %
      str(datetime.timedelta(seconds=(time.time() - start_time))))


all_grid = model.datacollector.get_model_vars_dataframe()
fig, axs = plt.subplots(figsize=(10, 10))
axs.set_xticks([])
axs.set_yticks([])
patch = plt.imshow(all_grid.iloc[0][0], cmap=plt.cm.binary)


def animate(i):
    patch.set_data(all_grid.iloc[i][0])


anim = animation.FuncAnimation(fig, animate, frames=MAX_ITERATIONS)
anim.save('Example05.gif', writer='imagemagick', fps=10)
