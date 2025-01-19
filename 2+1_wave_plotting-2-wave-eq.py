# doing all of the necessary imports
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc
import numpy as np


# ----- initialising the wave parameters -----
L = 30.0              # (system length)
dx = 0.3              # (discrete spatial stepsize for x-axis)
dy = dx               # (discrete spatial stepsize for y-axis)
c = 1.0               # (wave speed)
dt = 0.5 * dx / c     # (time stepsize)
sigma = 0.75           # (with of the pulse)
nsteps = 200          # (number of steps / frames for plotting)

(x_start, y_start) = (L / 2, L / 2)      # (center of the system, the point where the pulse will be applied)

# ----- style parameters for plotting -----
WIREFRAME_LINE_WIDTH = 0.2
WIREFRAME_COLOR = (0, 0, 0)


# ----- defining the arrays that store positions -----
x = np.arange(0, L, dx)
y = np.arange(0, L, dy)
xx, yy = np.meshgrid(x, y)

# ----- wave initialisation -----
phi = np.zeros((len(x), len(y), 3))  # (storage for t-1, t, and t+1)

npts = len(x)  # (number of spatial points)


# ----- doing the first step in the algorithm -----
phi[:, :, 1] = np.exp(-((xx - x_start)**2 + (yy - y_start)**2) / (2 * sigma**2))


# ----- setting up the plot -----
rc('animation', html='jshtml')
figure = plt.figure()
ax = figure.add_subplot(projection="3d")
plot_elements = [None]
ax.set_zlim(-0.25, 1)

ax.set_title("2+1 wave propagation")
ax.set_xlabel("x")
ax.set_ylabel("y")



# ----- update function for animation generation -----
def update(frame):
    global phi

    # Compute Laplacian (central differences)
    laplacian = (
        (phi[:-2, 1:-1, 1] + phi[2:, 1:-1, 1] - 2 * phi[1:-1, 1:-1, 1]) / dx**2 +
        (phi[1:-1, :-2, 1] + phi[1:-1, 2:, 1] - 2 * phi[1:-1, 1:-1, 1]) / dy**2
    )

    # Update the wave using finite differences
    phi[1:-1, 1:-1, 2] = (
        2 * phi[1:-1, 1:-1, 1] - phi[1:-1, 1:-1, 0] + c**2 * dt**2 * laplacian
    )

    # Update time slices
    phi[:, :, 0] = phi[:, :, 1]
    phi[:, :, 1] = phi[:, :, 2]

    # Update the plot
    ax.clear()
    ax.set_zlim(-0.25, 5)
    ax.set_title(f"2+1 wave propagation, Time = {frame * dt:.2f}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    plot_elements[0] = ax.plot_surface(xx, yy, phi[:, :, 2], cmap="viridis")

    print(f"Processing frame {frame}")

    return plot_elements


# ----- generating the animation -----
animation = FuncAnimation(figure, update, frames=nsteps, interval=50)

plt.show()