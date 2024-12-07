import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ====== setting up parameters ======
A = 1.0  # amplitude
(kx, ky) = (2 * np.pi / 10, 2 * np.pi / 10)  # wave vectors
omega = 2 * np.pi / 5  # angular frequency

# ====== creating the grid ======
x = np.linspace(0, 10, 200)
y = np.linspace(0, 10, 200)
(X, Y) = np.meshgrid(x, y)

# ====== initialising the grid ======
figure = plt.figure(figsize=(8, 8))
ax = figure.add_subplot(111, projection='3d')
ax.set_title("2D wave evolution")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("Amplitude")

# ====== plotting the initial step ======
t0 = 0
Z = A * np.cos(kx * X + ky * Y - omega * t0)
wave_surface = ax.plot_surface(X, Y, Z, cmap='viridis')

ax.set_zlim(-A, A)


# ====== update function for the animation ======
def update(t):
    ax.clear()
    Z = A * np.cos(kx * X + ky * Y - omega * t)
    wave_surface = ax.plot_surface(X, Y, Z, cmap='viridis')

    ax.set_title(f"2D wave evolution at t={t}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    ax.set_zlim(-A, A)  # Keep z-limits consistent

    return wave_surface


animation = FuncAnimation(figure, update, frames=np.linspace(0, 10, 100), interval=50)
plt.show()
