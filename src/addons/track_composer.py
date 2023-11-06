"""Utility for visual track generation. Meant for internal use only.

Author:
    Paulo Sanchez (@erlete)
"""


from itertools import cycle

import matplotlib.pyplot as plt


def ax_lim_auto(
    ax,
    x: list[int | float],
    y: list[int | float],
    z: list[int | float],
    offset: int | float
):
    """Set axis limits automatically.

    Args:
        ax (matplotlib.Axes.Axes): ax to set limits for.
        x (list[int | float]): x coordinates.
        y (list[int | float]): y coordinates.
        z (list[int | float]): z coordinates.
        offset (int | float): additional distance to add to limits.
    """
    centers = (
        (max(x) + min(x)) / 2,
        (max(y) + min(y)) / 2,
        (max(z) + min(z)) / 2
    )

    max_distance = max(
        abs(max(x) - min(x)) / 2,
        abs(max(y) - min(y)) / 2,
        abs(max(z) - min(z)) / 2
    )

    ax.set_xlim3d(
        centers[0] - max_distance - offset,
        centers[0] + max_distance + offset
    )
    ax.set_ylim3d(
        centers[1] - max_distance - offset,
        centers[1] + max_distance + offset
    )
    ax.set_zlim3d(
        centers[2] - max_distance - offset,
        centers[2] + max_distance + offset
    )


COLORS = cycle(["r", "g", "b", "m", "y", "k"])  # Cycling colors.

# Coordinate input:
x: list[int, float] = [0, 1, 2]
y: list[int, float] = [0, 1, 2]
z: list[int, float] = [0, 1, 2]

# Formatted output:
print(str({
    "start": [x[0], y[0], z[0]],
    "end": [x[-1], y[-1], z[-1]],
    "rings": [
        {
            "position": [x[i], y[i], z[i]],
            "rotation": [0, 0, 0]
        } for i in range(1, len(x) - 1)
    ]
}).replace("'", "\""))

# Figure and ax creation:
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Plotting:
ax.plot(x, y, z, "-")
for i in range(len(x)):
    ax.plot(x[i], y[i], z[i], "o", color=next(COLORS))

ax_lim_auto(ax, x, y, z, 1)
plt.show()
