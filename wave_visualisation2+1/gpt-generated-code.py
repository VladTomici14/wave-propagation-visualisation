# ----- doing all the necessary imports -----
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# ----- initializing the constants -----
L = 30.0  # Length of the system
dx = 0.3  # Spatial step size
c = 0.01  # Wave speed
dt = 0.5 * dx / c  # Time step (adjusted for stability)

# Initial condition: Gaussian pulse
x_start, y_start = L / 2, L / 2
w = 3.0  # Width of the Gaussian wave pulse

# ----- defining the grid -----
x = np.arange(0, L + dx, dx)
y = np.arange(0, L + dx, dx)
xx, yy = np.meshgrid(x, y)

npts = len(x)  # Number of spatial points
nsteps = 199  # Number of time steps

# Initialize wave (u) and velocity (v)
u = np.exp(-(xx - x_start) ** 2 / w ** 2) * np.exp(-(yy - y_start) ** 2 / w ** 2)
v = np.zeros_like(u)


# Function to compute Laplacian
def laplacian(f):
    return (
            (f[:-2, 1:-1] + f[2:, 1:-1] - 2 * f[1:-1, 1:-1]) / dx ** 2 +
            (f[1:-1, :-2] + f[1:-1, 2:] - 2 * f[1:-1, 1:-1]) / dx ** 2
    )


# Runge-Kutta 4th-order update
def rk4_step(u, v):
    padded_u = np.pad(u, 1, mode="constant", constant_values=0)

    k1_v = c ** 2 * laplacian(padded_u)
    k1_u = v[1:-1, 1:-1]

    k2_v = c ** 2 * laplacian(np.pad(u + 0.5 * dt * k1_u, 1, mode="constant", constant_values=0))
    k2_u = v[1:-1, 1:-1] + 0.5 * dt * k1_v

    k3_v = c ** 2 * laplacian(np.pad(u + 0.5 * dt * k2_u, 1, mode="constant", constant_values=0))
    k3_u = v[1:-1, 1:-1] + 0.5 * dt * k2_v

    k4_v = c ** 2 * laplacian(np.pad(u + dt * k3_u, 1, mode="constant", constant_values=0))
    k4_u = v[1:-1, 1:-1] + dt * k3_v

    u_next = u[1:-1, 1:-1] + (dt / 6) * (k1_u + 2 * k2_u + 2 * k3_u + k4_u)
    v_next = v[1:-1, 1:-1] + (dt / 6) * (k1_v + 2 * k2_v + 2 * k3_v + k4_v)

    return u_next, v_next


# Set up the plot
fig = plt.figure()
ax = fig.add_subplot(projection="3d")

# Initialize surface and wireframe
surface = ax.plot_surface(xx, yy, u, cmap=matplotlib.cm.coolwarm, rstride=1, cstride=1)
wireframe = ax.plot_wireframe(xx, yy, u, rstride=10, cstride=10, color='k', linewidth=0.2)

ax.set_zlim(-0.25, 1)
ax.set_title("Wave Propagation")
ax.set_xlabel("x")
ax.set_ylabel("y")


# Update function for animation
def update(frame):
    global u, v
    u[1:-1, 1:-1], v[1:-1, 1:-1] = rk4_step(u, v)

    # Update surface
    surface.remove()  # Remove old surface
    surface = ax.plot_surface(xx, yy, u, cmap=matplotlib.cm.coolwarm, rstride=1, cstride=1)

    print(f"Processing frame {frame}")
    return surface, wireframe


# Create animation
ani = FuncAnimation(fig, update, frames=nsteps, interval=50, blit=False)

# Show the animation
plt.show()
