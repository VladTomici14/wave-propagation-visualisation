import numpy as np
from vispy import scene
from vispy.scene import visuals
from vispy.app import Timer

# ----- Initialize constants -----
L = 30.0  # Length of the system
dx = 0.5  # Spatial step
c = 0.01  # Wave speed

# Initial Gaussian pulse parameters
x_start, y_start = L / 2, L / 2
w = 3.0

# Time step satisfying CFL condition
dt = 0.707 * dx / c

# Discretize space
x = np.arange(0, L + dx, dx)
y = np.arange(0, L + dx, dx)
xx, yy = np.meshgrid(x, y)
npts = len(x)

# Initialize the wave field
f = np.zeros((npts, npts, 3), dtype=np.float32)
f[:, :, 0] = np.exp(-(xx - x_start) ** 2 / w ** 2) * np.exp(-(yy - y_start) ** 2 / w ** 2)

# Compute the first time step
f[1:-1, 1:-1, 1] = (
    f[1:-1, 1:-1, 0]
    + 0.5 * c**2 * (f[:-2, 1:-1, 0] + f[2:, 1:-1, 0] - 2 * f[1:-1, 1:-1, 0]) * (dt**2 / dx**2)
    + 0.5 * c**2 * (f[1:-1, :-2, 0] + f[1:-1, 2:, 0] - 2 * f[1:-1, 1:-1, 0]) * (dt**2 / dx**2)
)

# ----- Set up Vispy Canvas -----
canvas = scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()
view.camera = 'turntable'

# 3D Surface plot
surface = visuals.SurfacePlot(x=x, y=y, z=f[:, :, 0], shading='smooth', color=(0.5, 0.5, 1, 1))
view.add(surface)

# Axes
axis = visuals.XYZAxis(parent=view.scene)

# Timer for animation
frame_index = 0

def update(event):
    global f, frame_index
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

    # Update the surface plot
    surface.set_data(z=f[:, :, 2])
    frame_index += 1

# Start animation
timer = Timer(interval=1 / 60, connect=update, start=True)

if __name__ == '__main__':
    canvas.app.run()
