
'''

    TC2008B - Prey - Depredator Model

    By:
        José Ángel Rico Mendieta - A01707404

    Date:
        2022-11-14

'''

# Imports
from mesa import Agent
import numpy as np

'''
    Agent Prey - Nonine

    Parameters:
        - unique_id: Unique ID of the agent
        - model: Model where the agent is located
        - x: X position of the agent
        - y: Y position of the agent
        - active: Active state of the agent
        - initial_energy: Initial energy of the agent (food)
        - max_capacity: Maximum capacity of the agent (food)
        - energy_rate: Energy rate of the agent (metabolism)
        - minimun_ege: Minimum age of the agent (reproduction)
        - rate_of_reproduction: Rate of reproduction of the agent (of food)
        - maximum_age: Maximum age of the agent (death)
        - energy_value: Energy value of the agent (when it's eaten for a deddian)
        - probability_reproduce: Probability of reproduction of the agent

    Atributes:
        - energy: Energy of the agent (food)
        - age: Age of the agent
        - type: Type of the agent
        - alive: Alive state of the agent
        
'''


class Nonine(Agent):
    def __init__(self, unique_id, model, x, y, active=True, initial_energy=10,
                 max_capacity=45, energy_rate=3, minimun_age=10, rate_of_reproduction=40,
                 maximum_age=25, energy_value=30, probability_reproduce=0.5):
        super().__init__(unique_id, model)
        self.model = model
        self.x = x
        self.y = y
        self.initial_energy = initial_energy
        self.max_capacity = max_capacity
        self.energy_rate = energy_rate
        self.minimun_age = minimun_age
        self.rate_of_reproduction = rate_of_reproduction
        self.maximum_age = maximum_age
        self.energy_value = energy_value
        self.probability_reproduce = probability_reproduce
        self.type = "Nonine"
        self.energy = self.initial_energy
        self.age = 0
        self.alive = 1
        self.active = active

    def is_alive(self):
        if self.age >= self.maximum_age:
            self.alive = 0
        if self.energy <= 0:
            self.alive = 0
        return self.alive == 1

    def move(self):

        new_position = random_position_empty(self)

        if new_position is None:
            return

        self.model.grid.move_agent(self, (new_position[0], new_position[1]))
        self.x = new_position[0]
        self.y = new_position[1]

    def eat(self):
        if self.energy >= self.max_capacity:
            return

        new_energy = self.model.floor[self.x][self.y]

        if new_energy + self.energy >= self.max_capacity:
            self.model.floor[self.x][self.y] = new_energy + \
                self.energy - self.max_capacity
            self.energy = self.max_capacity
            return

        self.energy += new_energy
        self.model.floor[self.x][self.y] = 0

    def reproduce(self):
        if not self.can_reproduce():
            return

        new_position = random_position_empty(self)

        if new_position is None:
            return

        new_energy = self.energy // 2

        new_agent = Nonine(self.model.next_id(), self.model,
                           new_position[0], new_position[1],
                           active=False, initial_energy=new_energy)
        self.model.grid.place_agent(
            new_agent, (new_position[0], new_position[1]))
        self.model.schedule.add(new_agent)
        self.energy = new_energy

    def can_reproduce(self):
        if self.age <= self.minimun_age:
            return False

        if self.energy <= self.rate_of_reproduction:
            return False

        if self.random.random() > self.probability_reproduce:
            return False

        for content in self.model.grid.get_neighbors(self.pos, moore=False, include_center=False):
            if content is not None:
                if content.type == "Deddian":
                    return False

        return True

    def step(self):
        if self.is_alive() and self.active:
            self.move()
            self.eat()
            self.reproduce()
            self.age += 1
            self.energy -= self.energy_rate


'''
    Agent Depredator - Deddian

    Parameters:
        - unique_id: Unique ID of the agent
        - model: Model where the agent is located
        - x: X position of the agent
        - y: Y position of the agent
        - active: Active state of the agent
        - initial_energy: Initial energy of the agent (food)
        - max_capacity: Maximum capacity of the agent (food)
        - energy_rate: Energy rate of the agent (metabolism)
        - probability_reproduce: Probability of reproduction of the agent
        - minimun_age: Minimum age of the agent (reproduction)
        - minimum_energy: Minimum energy of the agent (reproduction)
        - maximum_age: Maximum age of the agent (death)

    Atributes:
        - energy: Energy of the agent (food)
        - age: Age of the agent
        - type: Type of the agent
        - alive: Alive state of the agent
'''


class Deddian(Agent):
    def __init__(self, unique_id, model, x, y, active=True, initial_energy=150,
                 max_capacity=200, energy_rate=3, probability_reproduce=0.5, minimun_age=10,
                 minimum_energy=120, maximum_age=50):
        super().__init__(unique_id, model)
        self.model = model
        self.x = x
        self.y = y
        self.max_capacity = max_capacity
        self.energy_rate = energy_rate
        self.probability_reproduce = probability_reproduce
        self.minimun_age = minimun_age
        self.minimum_energy = minimum_energy
        self.maximum_age = maximum_age
        self.initial_energy = initial_energy
        self.type = "Deddian"
        self.energy = self.initial_energy
        self.age = 0
        self.active = active
        self.alive = 1

    def is_alive(self):
        if self.age >= self.maximum_age:
            self.alive = 0
        if self.energy <= 0:
            self.alive = 0
        return self.alive == 1

    def move(self):
        new_position = self.random_position()

        if new_position is None:
            return

        if self.model.grid.is_cell_empty((new_position[0], new_position[1])):
            self.model.grid.move_agent(
                self, (new_position[0], new_position[1]))
            self.x = new_position[0]
            self.y = new_position[1]
            return

        self.eat(new_position[0], new_position[1])

    def eat(self, x, y):
        if self.energy >= self.max_capacity:
            return

        if self.model.grid[x][y].alive != 0:
            self.energy += self.model.grid[x][y].energy_value

        self.model.delete_agent(self.model.grid[x][y])

        self.model.grid.move_agent(self, (x, y))
        self.x = x
        self.y = y

    def reproduce(self):
        if self.age <= self.minimun_age:
            return

        if self.energy <= self.minimum_energy:
            return

        if self.random.random() > self.probability_reproduce:
            return

        new_position = random_position_empty(self)

        if new_position is None:
            return

        new_energy = self.energy // 2

        new_agent = Deddian(self.model.next_id(), self.model,
                            new_position[0], new_position[1], active=False, initial_energy=new_energy)
        self.model.grid.place_agent(
            new_agent, (new_position[0], new_position[1]))
        self.model.schedule.add(new_agent)
        self.energy = new_energy

    def random_position(self):
        empty_cells = []
        for (x, y) in self.model.grid.iter_neighborhood(
                self.pos, moore=False, include_center=False):
            if self.model.grid.is_cell_empty((x, y)) or self.model.grid.get_cell_list_contents((x, y))[0].type == "Nonine":
                empty_cells.append([x, y])

        if len(empty_cells) == 0:
            return None

        return self.random.choice(empty_cells)

    def step(self):
        if self.is_alive() and self.active:
            self.move()
            self.reproduce()
            self.age += 1
            self.energy -= self.energy_rate


def random_position_empty(self):
    empty_cells = []
    for (x, y) in self.model.grid.iter_neighborhood(
            self.pos, moore=False, include_center=False):
        if self.model.grid.is_cell_empty((x, y)):
            empty_cells.append([x, y])

    if len(empty_cells) == 0:
        return None

    return self.random.choice(empty_cells)
