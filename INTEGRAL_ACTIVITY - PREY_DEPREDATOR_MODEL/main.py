
from System.Model import Cenitune
import time
import datetime
import matplotlib.animation as animation
import matplotlib.pyplot as plt

MAX_ITERATIONS = 200

start_time = time.time()
Model = Cenitune()

i = 0
while i <= MAX_ITERATIONS:
    Model.step()
    i += 1

print("Time executation: ", str(
    datetime.timedelta(seconds=(time.time() - start_time))))

all_grids = Model.datacollector.get_model_vars_dataframe()

fig, axis = plt.subplots(figsize=(7, 7))
axis.set_xticks([])
axis.set_yticks([])
patch = axis.imshow(all_grids.iloc[0][0], cmap=plt.cm.binary)


def animate(i):
    patch.set_data(all_grids.iloc[i][0])


anim = animation.FuncAnimation(
    fig, animate, frames=len(all_grids), interval=100)
anim.save(' Simulation of the Prey - Depredator Model.gif',
          writer='imagemagick', fps=10)
print("Simulation of the Prey - Depredator Model.gif ready")
