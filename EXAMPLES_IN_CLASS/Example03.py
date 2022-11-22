import time
import datetime
import numpy as np
import pandas as pd
from mesa import Agent, Model
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.rcParams['animation.html'] = 'jshtml'
matplotlib.rcParams['animation.embed_limit'] = 2**128

print("Starting execute: 'Ejemplo 03: Modelo de juego de la vida'")


class GameLifeAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.alive = np.random.choice([0, 1])
        self.next_state = None

    def step(self):
        live_neighbours = 0

        for neighbour in self.model.grid.neighbor_iter(self.pos):
            live_neighbours += neighbour.alive

        self.next_state = self.alive
        if self.next_state == 1:
            if live_neighbours < 2 or live_neighbours > 3:
                self.next_state = 0
        else:
            if live_neighbours == 3:
                self.next_state = 1

    def advance(self):
        self.alive = self.next_state


def get_grid(model):
    grid = np.zeros((model.grid.width, model.grid.height))
    for (content, x, y) in model.grid.coord_iter():
        grid[x][y] = content.alive
    return grid


class GameLifeModel(Model):
    def __init__(self, width, height, ):
        self.num_agents = width * height
        self.grid = SingleGrid(width, height, torus=True)
        self.schedule = SimultaneousActivation(self)
        self.datacollector = DataCollector(
            model_reporters={"Grid": get_grid})

        for (content, x, y) in self.grid.coord_iter():
            a = GameLifeAgent((x, y), self)
            self.grid.place_agent(a, (x, y))
            self.schedule.add(a)

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()


GRID_SIZE = 100
MAX_GENERATIONS = 100

start_time = time.time()
model = GameLifeModel(GRID_SIZE, GRID_SIZE)
for i in range(MAX_GENERATIONS):
    model.step()
print("Execution time: %s seconds" % str((time.time() - start_time)))


all_grid = model.datacollector.get_model_vars_dataframe()

fig, axis = plt.subplots(figsize=(10, 10))
axis.set_xticks([])
axis.set_yticks([])
patch = axis.imshow(all_grid.iloc[0][0], cmap=plt.cm.binary)


def animate(i):
    patch.set_data(all_grid.iloc[i][0])


anim = animation.FuncAnimation(
    fig, animate, frames=MAX_GENERATIONS, interval=100)
anim.save('Ejemplo03.gif', writer='imagemagick', fps=10)

print("Finished execute: 'Ejemplo 03: Modelo de juego de la vida'")
