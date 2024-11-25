import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Initialize physical and numerical constants

a = 1.0  # set the length of the system
dx = 0.1  # set the discrete spatial stepsize
c = 1.0  # define the wave speed

dt = dx / c  # choose a time step to satisfy the CFL condition. Information can't
# travel further than dx during a time dt or the system will be
# numerically unstable.

x = np.arange(0, a * (1 + dx), dx)  # define an array to store x position data
npts = len(x)  # this is the number of spatial points along x
nsteps = 100  # set the number of time steps

f = np.zeros((npts, 3))

xc = 0.5  # define the center of the system to locate a Gaussian pulse (see below)
w = 0.05  # define the width of the Gaussian wave pulse

# f[:,0] = np.exp(-(x-xc)**2/(w**2)) #use this initial condition for a Gaussian
f[:, 0] = np.sin(2 * np.pi * x / a)  # use this initial condition for a standing wave

# first time step in the leap frog algorithm
f[1:-1, 1] = f[1:-1, 0] + .5 * c ** 2 * (f[:-2, 0] + f[2:, 0] - 2. * f[1:-1, 0]) * (dt ** 2 / dx ** 2)

# ----- setting up the plot -----
fig, ax = plt.subplots()
line, = ax.plot(x, f[:, 0], 'b')  # Line to update in the animation
ax.set_xlim(0, 1)
ax.set_ylim(-1.5, 1.5)
ax.set_title('Wave Propagation')
ax.set_xlabel('x')
ax.set_ylabel('Amplitude')


# ----- update function -----
def update(frame):
    global f
    f[1:-1, 2] = -f[1:-1, 0] + 2 * f[1:-1, 1] \
                 + c ** 2 * (f[:-2, 1] + f[2:, 1] - 2.0 * f[1:-1, 1]) * (dt ** 2 / dx ** 2)

    # Leapfrog update
    f[:, 0] = f[:, 1]
    f[:, 1] = f[:, 2]

    # Enforce boundary conditions
    f[0, :] = 0
    f[-1, :] = 0

    line.set_ydata(f[:, 2])  # Update the y-data of the line
    ax.set_title(f't = {frame * dt:.2f}')
    return line,


# Create animation
ani = FuncAnimation(fig, update, frames=nsteps, interval=50, blit=True)

# Show animation
plt.show()
