import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Initialize physical and numerical constants
L = 1.0  # length of the system
dx = 0.01  # discrete spatial stepsize
c = 1.0  # wave speed

dt = 0.707 * dx / c  # time step satisfying the CFL condition
x = np.arange(0, L * (1 + dx), dx)
y = np.arange(0, L * (1 + dx), dx)

xx, yy = np.meshgrid(x, y)
npts = len(x)  # number of spatial points
nsteps = 199  # number of time steps

f = np.zeros((npts, npts, 3))

# Initial condition: Gaussian pulse
xc = 0.5  # center of the system
w = 0.05  # width of the Gaussian wave pulse
f[:, :, 0] = np.exp(-(xx - xc) ** 2 / w ** 2) * np.exp(-(yy - xc) ** 2 / w ** 2)

# First time step in the leapfrog algorithm
f[1:-1, 1:-1, 1] = (
    f[1:-1, 1:-1, 0]
    + 0.5 * c**2 * (f[:-2, 1:-1, 0] + f[2:, 1:-1, 0] - 2 * f[1:-1, 1:-1, 0]) * (dt**2 / dx**2)
    + 0.5 * c**2 * (f[1:-1, :-2, 0] + f[1:-1, 2:, 0] - 2 * f[1:-1, 1:-1, 0]) * (dt**2 / dx**2)
)

# Set up the plot
fig = plt.figure()
ax = fig.add_subplot(projection="3d")
plot_elements = [  # Use a mutable container to hold plot elements
    ax.plot_surface(xx, yy, f[:, :, 0], cmap=cm.coolwarm, rstride=1, cstride=1),
    ax.plot_wireframe(xx, yy, f[:, :, 0], rstride=10, cstride=10, color="green"),
]
ax.set_zlim(-0.25, 1)
ax.set_title("Wave Propagation")
ax.set_xlabel("x")
ax.set_ylabel("y")

# Update function for animation
def update(frame):
    global f
    # Leapfrog algorithm
    f[1:-1, 1:-1, 2] = (
        -f[1:-1, 1:-1, 0]
        + 2 * f[1:-1, 1:-1, 1]
        + c**2 * (f[:-2, 1:-1, 1] + f[2:, 1:-1, 1] - 2 * f[1:-1, 1:-1, 1]) * (dt**2 / dx**2)
        + c**2 * (f[1:-1, :-2, 1] + f[1:-1, 2:, 1] - 2 * f[1:-1, 1:-1, 1]) * (dt**2 / dx**2)
    )

    # Update for next time step
    f[:, :, 0] = f[:, :, 1]
    f[:, :, 1] = f[:, :, 2]

    # Remove and update the plot
    for element in plot_elements:
        element.remove()
    plot_elements[0] = ax.plot_surface(xx, yy, f[:, :, 2], cmap=cm.coolwarm, rstride=1, cstride=1)
    plot_elements[1] = ax.plot_wireframe(xx, yy, f[:, :, 2], rstride=10, cstride=10, color="green")
    ax.set_title(f"t = {frame * dt:.2f}")
    return plot_elements

# Create animation
ani = FuncAnimation(fig, update, frames=nsteps, interval=50, blit=False)

# Show the animation
plt.show()
