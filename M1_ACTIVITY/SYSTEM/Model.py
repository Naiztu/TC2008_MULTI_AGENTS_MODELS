'''

    TC2008B - M1 - Activity 1

    By:
        José Ángel Rico Mendieta - A01707404

    Date:
        2022-11-22

'''
from SYSTEM.Agents import RobotVacuumCleanerAgent
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import numpy as np

LIMIT = 10000


def get_grid(model):
    grid = np.zeros((model.grid.width, model.grid.height))
    for x in range(model.grid.width):
        for y in range(model.grid.height):
            if model.grid.is_cell_empty((x, y)):
                grid[x][y] = model.floor[x][y] * 2
            else:
                grid[x][y] = 1
    return grid

'''
    Model RobotVacuumCleanerModel

    This model is the one that will be managing the agents and the grid.

    Parameters:
        - width: Width of the grid
        - height: Height of the grid
        - num_agents: Number of robots that will be in the grid
        - dirty_cells_percentage: Percentage of dirty cells in the grid

    Attributes:
        - grid: Grid of the model
        - schedule: Schedule of the model
        - datacollector: Datacollector of the model
        - floor: Floor of the model


'''
class RobotVacuumCleanerModel(Model):
    def __init__(self, width, height, num_agents, dirty_cells_percentage=0.5):
        self.num_agents = num_agents
        self.dirty_cells_percentage = dirty_cells_percentage
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.floor = np.zeros((width, height))

        for i in range(self.num_agents):
            a = RobotVacuumCleanerAgent(i, self)
            self.grid.place_agent(a, (1, 1))
            self.schedule.add(a)

        amount = int((width * height) * dirty_cells_percentage)
        for i in range(amount):
            finished = False
            while not finished:
                x = int(np.random.rand() * LIMIT) % width
                y = int(np.random.rand() * LIMIT) % height
                if self.floor[x][y] == 0:
                    self.floor[x][y] = 1
                    finished = True

        self.datacollector = DataCollector(model_reporters={"Grid": get_grid})

    def is_all_clean(self):
        return np.all(self.floor == 0)

    def get_info(self):
        print("Number of agents: ", self.num_agents)
        print("Dirty cells percentage: ", self.dirty_cells_percentage)
        print("Grid size: ", self.grid.width, "x", self.grid.height)
        for agent in self.schedule.agents:
            print("Agent", agent.unique_id, "moviments: ", agent.moviments)

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.dirty_cells_percentage = np.count_nonzero(
            self.floor) / (self.grid.width * self.grid.height)
