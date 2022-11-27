'''

    TC2008B - M1 - Activity 1

    By:
        José Ángel Rico Mendieta - A01707404

    Date:
        2022-11-22

'''

from SYSTEM.Model import RobotVacuumCleanerModel
import time
import matplotlib.animation as animation
import matplotlib.pyplot as plt

WIDTH_GRID = 20  # Width of the grid
HEIGHT_GRID = 30  # Height of the grid
NUM_ROBOTS = 10  # Number of robots
DIRTY_CELLS_PERCENTAGE = 0.5  # Percentage of dirty cells in the grid
MAX_STEPS = 200  # Time of execution maximum in seconds
FLAG_FINALIZED = False # Flag of the simulation is will finished completely

start_time = time.time()
model = RobotVacuumCleanerModel(
    HEIGHT_GRID, WIDTH_GRID, NUM_ROBOTS, DIRTY_CELLS_PERCENTAGE, FLAG_FINALIZED, MAX_STEPS)

while not model.is_finalized():
    model.step()


time_execution = time.time() - start_time

model.get_info()
print("Time of execution: %s seconds" % round(time_execution, 2))

all_grids = model.datacollector.get_model_vars_dataframe()
fig, axs = plt.subplots(figsize=(7, 7))
axs.set_xticks([])
axs.set_yticks([])
patch = plt.imshow(all_grids.iloc[0][0], cmap="gray")


def animate(i):
    patch.set_data(all_grids.iloc[i][0])


anim = animation.FuncAnimation(
    fig, animate, frames=len(all_grids), interval=100)
anim.save('Animation.gif', writer='imagemagick', fps=10)
