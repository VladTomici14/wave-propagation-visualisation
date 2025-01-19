# ----- doing all of the necessary imports -----
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc
import numpy as np

# ----- initialising the wave parameters -----
L = 30.0              # (system length)
dx = 0.3              # (discrete spatial stepsize)
c = 1                 # (wave speed)
dt = 0.707 * dx / c   # (time stepsize)
w = 3.0               # (with of the pulse)

# (center of the system, the point where the pulse will be applied)
(x_start, y_start) = (L / 2, L / 2)

# ----- style parameters for plotting -----
WIREFRAME_LINE_WIDTH = 0.2
WIREFRAME_COLOR = (0, 0, 0)

# ----- defining the arrays that store positions -----
x = np.arange(0, L * (1 + dx), dx)
y = np.arange(0, L * (1 + dx), dx)

xx, yy = np.meshgrid(x, y)

npts = len(x)  # (number of spatial points)
nsteps = 199   # (number of time steps)

# ----- doing the first step in the algorithm -----
f = np.zeros((npts, npts, 3))
f[:, :, 0] = np.exp(-(xx - x_start) ** 2 / w ** 2) * np.exp(-(yy - y_start) ** 2 / w ** 2)

f[1:-1, 1:-1, 1] = (
    f[1:-1, 1:-1, 0]
    + 0.5 * c**2 * (f[:-2, 1:-1, 0] + f[2:, 1:-1, 0] - 2 * f[1:-1, 1:-1, 0]) * (dt**2 / dx**2)
    + 0.5 * c**2 * (f[1:-1, :-2, 0] + f[1:-1, 2:, 0] - 2 * f[1:-1, 1:-1, 0]) * (dt**2 / dx**2)
)

# ----- setting up the plot -----
rc('animation', html='jshtml')
figure = plt.figure()
ax = figure.add_subplot(projection="3d")
plot_elements = [None, None]
ax.set_zlim(-0.25, 1)

ax.set_title("2+1 wave propagation")
ax.set_xlabel("x")
ax.set_ylabel("y")


# ----- update function for animation generation -----
def update(frame):
    global f

    # ----- leapfrog algorithm -----
    f[1:-1, 1:-1, 2] = (
            -f[1:-1, 1:-1, 0] + 2 * f[1:-1, 1:-1, 1]
            + c ** 2 * (f[:-2, 1:-1, 1] + f[2:, 1:-1, 1] - 2 * f[1:-1, 1:-1, 1]) * (dt ** 2 / dx ** 2)
            + c ** 2 * (f[1:-1, :-2, 1] + f[1:-1, 2:, 1] - 2 * f[1:-1, 1:-1, 1]) * (dt ** 2 / dx ** 2)
    )

    # ----- update for next time step -----
    f[:, :, 0] = f[:, :, 1]
    f[:, :, 1] = f[:, :, 2]

    # ----- updating the plot -----
    if plot_elements[0]:
        plot_elements[0].remove()
    if plot_elements[1]:
        plot_elements[1].remove()

    plot_elements[0] = ax.plot_surface(xx, yy, f[:, :, 2], cmap=matplotlib.cm.coolwarm, rstride=1, cstride=1)
    plot_elements[1] = ax.plot_wireframe(xx, yy, f[:, :, 2], rstride=10, cstride=10, color=WIREFRAME_COLOR, linewidth=WIREFRAME_LINE_WIDTH)
    ax.set_title(f"t = {frame * dt:.2f}")

    print(f"Processing frame {frame}")

    return plot_elements


# ----- generating the animation -----
animation = FuncAnimation(figure, update, frames=nsteps, interval=50, blit=False)

# ----- plotting the video animation -----
plt.show()