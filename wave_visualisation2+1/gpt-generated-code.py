import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# Parameters
Lx, Ly = 10, 10  # Dimensions of the grid (in space)
Nx, Ny = 100, 100  # Number of grid points in x and y directions
Tmax = 10  # Maximum time to simulate
c = 1  # Wave speed
dx = Lx / Nx  # Grid spacing in x direction
dy = Ly / Ny  # Grid spacing in y direction
dt = 0.1  # Time step
alpha = c * dt / dx  # Stability condition factor
nsteps = 199

# Discretization grids for space and time
x = np.linspace(0, Lx, Nx)
y = np.linspace(0, Ly, Ny)
X, Y = np.meshgrid(x, y)


# Initial condition - Gaussian pulse centered in the domain
def initial_condition(X, Y):
    return np.exp(-((X - Lx / 2) ** 2 + (Y - Ly / 2) ** 2) / 0.5)


# Initialize the wave function u(x, y, t) at time t = 0
u = initial_condition(X, Y)
u_new = np.zeros_like(u)
u_old = u.copy()

# Setup the figure for the animation
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Create the initial surface plot
surf = ax.plot_surface(X, Y, u, cmap='viridis')

# Set the labels and the title
ax.set_zlim(-1, 1)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('u(x, y, t)')


# Update function for animation
def update_wave(frame):
    global u, u_new, u_old, surf

    # Compute the next time step using finite difference for the wave equation
    u_new[1:-1, 1:-1] = 2 * u[1:-1, 1:-1] - u_old[1:-1, 1:-1] + alpha ** 2 * (
            u[2:, 1:-1] + u[:-2, 1:-1] + u[1:-1, 2:] + u[1:-1, :-2] - 4 * u[1:-1, 1:-1]
    )

    # Update the old and current wave functions
    u_old = u.copy()
    u = u_new.copy()

    # Update the Z data of the surface plot (no need to clear the plot)
    surf.remove()  # Remove the old surface plot
    surf = ax.plot_surface(X, Y, u, cmap='viridis')

    print(f"current surf: {surf}        current u: {u_new}")

    ax.set_title(f"Wave at time = {frame * dt:.2f}")


# Create the animation
ani = animation.FuncAnimation(fig, update_wave, frames=nsteps, interval=50, blit=False)
plt.show()
