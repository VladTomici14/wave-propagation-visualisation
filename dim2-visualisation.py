# ----- doing all the necessary imports -----
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# ----- initialising the constants -----
# length of the system
L = 30.0

# discrete spatial stepsize
dx = 0.3

# wave speed
c = 0.01

# Initial condition: Gaussian pulse
# center of the system
x_start = L / 2
y_start = L / 2

# width of the Gaussian wave pulse
w = 3.0

# ----- style constants -----
WIREFRAME_LINE_WIDTH = 0.2
WIREFRAME_COLOR = (0, 0, 0)

# ----- choosing a time step to satisfy the CFL condition -----
dt = 0.707 * dx / c  # time step satisfying the CFL condition

# ----- defining the arrays that store positions -----
x = np.arange(0, L * (1 + dx), dx)
y = np.arange(0, L * (1 + dx), dx)

xx, yy = np.meshgrid(x, y)

npts = len(x)  # number of spatial points
nsteps = 199  # number of time steps

f = np.zeros((npts, npts, 3))
f[:, :, 0] = np.exp(-(xx - x_start) ** 2 / w ** 2) * np.exp(-(yy - y_start) ** 2 / w ** 2)

# First time step in the leapfrog algorithm
f[1:-1, 1:-1, 1] = (
    f[1:-1, 1:-1, 0]
    + 0.5 * c**2 * (f[:-2, 1:-1, 0] + f[2:, 1:-1, 0] - 2 * f[1:-1, 1:-1, 0]) * (dt**2 / dx**2)
    + 0.5 * c**2 * (f[1:-1, :-2, 0] + f[1:-1, 2:, 0] - 2 * f[1:-1, 1:-1, 0]) * (dt**2 / dx**2)
)

# Set up the plot
fig = plt.figure()
ax = fig.add_subplot(projection="3d")
# plot_elements = [  # Use a mutable container to hold plot elements
#     ax.plot_surface(xx, yy, f[:, :, 0], cmap=matplotlib.cm.coolwarm, rstride=1, cstride=1),
#     ax.plot_wireframe(xx, yy, f[:, :, 0], rstride=10, cstride=10, linewidth=0),
# ]

plot_elements = [None, None]  # Ensure plot_elements is always defined as a list
ax.set_zlim(-0.25, 1)
ax.set_title("Wave Propagation")
ax.set_xlabel("x")
ax.set_ylabel("y")

# Update function for animation
def update(frame):
    global f
    # Leapfrog algorithm
    f[1:-1, 1:-1, 2] = (
            -f[1:-1, 1:-1, 0] + 2 * f[1:-1, 1:-1, 1]
            + c ** 2 * (f[:-2, 1:-1, 1] + f[2:, 1:-1, 1] - 2 * f[1:-1, 1:-1, 1]) * (dt ** 2 / dx ** 2)
            + c ** 2 * (f[1:-1, :-2, 1] + f[1:-1, 2:, 1] - 2 * f[1:-1, 1:-1, 1]) * (dt ** 2 / dx ** 2)
    )

    # Update for next time step
    f[:, :, 0] = f[:, :, 1]
    f[:, :, 1] = f[:, :, 2]

    # ===== updating the plot =====
    if plot_elements[0]:
        plot_elements[0].remove()
    if plot_elements[1]:
        plot_elements[1].remove()

    plot_elements[0] = ax.plot_surface(xx, yy, f[:, :, 2], cmap=matplotlib.cm.coolwarm, rstride=1, cstride=1)
    plot_elements[1] = ax.plot_wireframe(xx, yy, f[:, :, 2], rstride=10, cstride=10, color=WIREFRAME_COLOR, linewidth=WIREFRAME_LINE_WIDTH)
    ax.set_title(f"t = {frame * dt:.2f}")

    print(f"Processing frame {frame}")

    return plot_elements

# Create animation
ani = FuncAnimation(fig, update, frames=nsteps, interval=50, blit=False)

# Show the animation
plt.show()