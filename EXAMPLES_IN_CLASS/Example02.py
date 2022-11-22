import matplotlib
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

from mesa import Agent, Model
from mesa.time import RandomActivation

from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
# Lotes de trabajo, cuando mando pequeños fragmentos de cosas muy complejas
from mesa.batchrunner import BatchRunner

class MoneyAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1

    def step(self):  # Intercambiar la riqueza con otro agente
        if self.wealth > 0:
            other_agent = self.random.choice(self.model.schedule.agents)
            other_agent.wealth += 1
            self.wealth -= 1

class MoneyModel(Model):
    def __init__(self, num_agents):
        self.num_agents = num_agents
        self.schedule = RandomActivation(self)

        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)

    def step(self):
        self.schedule.step()

model = MoneyModel(10)
for i in range(10):
    model.step()

agents_wealth = [agent.wealth for agent in model.schedule.agents]
plt.hist(agents_wealth)

all_wealth = []
for i in range(100):

    model = MoneyModel(10)
    for j in range(10):
        model.step()
    for agent in model.schedule.agents:
        all_wealth.append(agent.wealth)

plt.hist(all_wealth, bins=range(max(all_wealth)+1))



