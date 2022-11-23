'''

    TC2008B - M1 - Activity 1

    By:
        José Ángel Rico Mendieta - A01707404

    Date:
        2022-11-22

'''
from mesa import Agent
import numpy as np

'''
    Agent RobotVacuumCleanerAgent

    This agent is the one that will be moving around the grid and cleaning the dirty cells.

    Parameters:
        - unique_id: Unique ID of the agent
        - model: Model that the agent belongs to
    
    Attributes:
        - moviments: Number of moviments that the agent has made
        - options: Options that the agent has to move

'''


class RobotVacuumCleanerAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.moviments = 0
        self.options = np.array([[-1, -1], [-1,  0], [-1, +1],
                                 [0, -1],           [0, +1],
                                 [+1, -1], [+1,  0], [+1, +1]])

    def random_position(self):
        option = self.random.choice(self.options)

        new_position = (self.pos[0] + option[0], self.pos[1] + option[1])

        if self.model.grid.out_of_bounds(new_position):
            return None

        return new_position

    def step(self):
        if self.model.floor[self.pos[0]][self.pos[1]] == 1:
            self.model.floor[self.pos[0]][self.pos[1]] = 0
        else:
            new_position = self.random_position()

            if new_position is None:
                return

            self.model.grid.move_agent(self, new_position)
            self.pos = new_position
            self.moviments += 1
