'''

    TC2008B - Prey - Depredator Model

    By:
        José Ángel Rico Mendieta - A01707404

    Date:
        2022-11-14

'''

# Imports
from System.Agents import Nonine, Deddian
from mesa import Model
from mesa.time import RandomActivationByType, RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
import numpy as np

'''
    Model Planet - Cenitune

    Parameters:
        - width: Width of the model
        - height: Height of the model
        - initial_nonines: Initial number of Nonines
        - initial_deddians: Initial number of Deddians
        - initial_herb: Initial number of Herb

    Atributes:
        - schedule: Schedule of the model
        - grid: Grid of the model
        - datacollector: Datacollector of the model
        - floor: Floor of the model(with herb)
        - current_id: Current ID of the model

'''


class Cenitune(Model):
    def __init__(self, width=35, height=35, initial_nonines=47, initial_deddians=15,
            initial_herb=20):
        self.width = width
        self.height = height
        self.num_nonines = initial_nonines
        self.num_dedians = initial_deddians
        self.num_herb = initial_herb
        self.current_id = 0

        self.floor = np.zeros((self.width, self.height))
        self.floor.fill(self.num_herb)

        self.grid = SingleGrid(self.width, self.height, False)

        self.schedule = RandomActivationByType(self)
        self.datacollector = DataCollector(
            model_reporters={"Grid": get_grid}
        )

        fill_agents(self, Deddian, self.num_dedians)
        fill_agents(self, Nonine, self.num_nonines)

    def grow(self):
        ones = np.ones((self.width, self.height))
        self.floor = np.add(self.floor, ones)

    def next_id(self):
        self.current_id += 1
        return self.current_id

    def activate(self):
        for agent in self.schedule.agents:
            if agent.active == False:
                agent.active = True

    def clean_deaths(self):
        for agent in self.schedule.agents:
            if agent.alive == 0:
                self.delete_agent(agent)

    def finish(self):
        return self.grid.exists_empty_cells()

    def step(self):
        self.datacollector.collect(self)
        self.clean_deaths()
        self.activate()
        self.schedule.step(False, True)
        self.grow()

    def delete_agent(self, agent):
        self.grid.remove_agent(agent)
        self.schedule.remove(agent)


def get_grid(model):
    grid = np.zeros((model.width, model.height))

    for (content, x, y) in model.grid.coord_iter():
        if content is None:
            continue
        elif content.alive != 1:
            continue
        elif content.type == "Nonine":
            grid[x][y] = 3
            continue
        elif content.type == "Deddian":
            grid[x][y] = 5
    return grid


def fill_agents(model, Agent, number):
    while number > 0:
        x = np.random.randint(0, model.grid.width)
        y = np.random.randint(0, model.grid.height)
        if model.grid.is_cell_empty((x, y)):
            new_agent = Agent(model.next_id(), model, x, y)
            model.grid.place_agent(new_agent, (x, y))
            model.schedule.add(new_agent)
            number -= 1
