import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from src.sdc.modules.core.gradient import ColorGradient

# Define the vertices of the cube in a NumPy array
vertices = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 1, 1]
])

# Define the edges of the cube
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# Create a figure and plot the cube
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the edges of the cube using the vertices
# for edge in edges:
#     x_values = [vertices[edge[0]][0], vertices[edge[1]][0]]
#     y_values = [vertices[edge[0]][1], vertices[edge[1]][1]]
#     z_values = [vertices[edge[0]][2], vertices[edge[1]][2]]
#     ax.plot(x_values, y_values, z_values, color='b')

x = np.array([[vertices[edge[0]][0], vertices[edge[1]][0]] for edge in edges])
y = np.array([[vertices[edge[0]][1], vertices[edge[1]][1]] for edge in edges])
z = np.array([[vertices[edge[0]][2], vertices[edge[1]][2]] for edge in edges])

for x0, y0, z0 in zip(x, y, z):
    ax.plot(x0, y0, z0, color='r')

# plot the center in blue


center = np.array([
    max(vertices[:, 0]) / 2,
    max(vertices[:, 1]) / 2,
    max(vertices[:, 2]) / 2
])

ax.plot(
    max(vertices[:, 0]) / 2,
    max(vertices[:, 1]) / 2,
    max(vertices[:, 2]) / 2,
    marker='o',
    color='g'
)

for i in range(0, 361, 15):
    rotation = [0, 0, i]
    rotation = [np.deg2rad(i) for i in rotation]

    azimuth, elevation, yaw = rotation

    rotation_matrix = np.array([
        [
            np.cos(azimuth) * np.cos(elevation),
            (
                np.cos(azimuth) * np.sin(elevation) * np.sin(yaw)
                - np.sin(azimuth) * np.cos(yaw)
            ),
            np.cos(azimuth) * np.sin(elevation) * np.cos(yaw)
            + np.sin(azimuth) * np.sin(yaw)
        ], [
            np.sin(azimuth) * np.cos(elevation),
            (
                np.sin(azimuth) * np.sin(elevation) * np.sin(yaw)
                + np.cos(azimuth) * np.cos(yaw)
            ),
            np.sin(azimuth) * np.sin(elevation) * np.cos(yaw)
            - np.cos(azimuth) * np.sin(yaw)
        ], [
            -np.sin(elevation),
            np.cos(elevation) * np.sin(yaw),
            np.cos(elevation) * np.cos(yaw)
        ]
    ])

    def Rx(theta):
        return np.matrix([
            [1, 0, 0],
            [0, np.cos(theta), -np.sin(theta)],
            [0, np.sin(theta), np.cos(theta)]
        ])
    def Ry(theta):
        return np.matrix([
            [np.cos(theta), 0, np.sin(theta)],
            [0, 1, 0],
            [-np.sin(theta), 0, np.cos(theta)]
        ])
    def Rz(theta):
        return np.matrix([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1]
        ])

    v1 = np.array([1, 0, 0])
    v2 = np.array([0, 1, 0])
    v3 = np.array([0, 0, 1])

    v1r = np.array(np.dot(Rx(rotation[0]), v1))[0]
    v2r = np.array(np.dot(Ry(rotation[1]), v2))[0]
    v3r = np.array(np.dot(Rz(rotation[2]), v3))[0]

    plt.plot(
        [0, v1r[0]],
        [0, v1r[1]],
        [0, v1r[2]],
        ".-",
        color='c',
        ms=10
    )

    point = np.array([1, 0, 0])
    R = Rz(rotation[2]) * Ry(rotation[1]) * Rx(rotation[0])

    # ax.plot(
    #     [0, point[0]],
    #     [0, point[1]],
    #     [0, point[2]],
    #     ".-",
    #     color='darkorange',
    #     ms=10
    # )

    # rotate the point using the R matrix
    point = np.array(np.array(np.dot(R, point))[0])
    # now use rotation_matrix

    print(point)

    ax.plot(
        [0, point[0]],
        [0, point[1]],
        [0, point[2]],
        ".-",
        color='r',
        ms=10
    )

    # x = center
    # u = np.array([np.pi/4, np.pi/4, 0])
    # u = rotation
    # ax.quiver(
    #     x[0], x[1], x[2],
    #     u[0], u[1], u[2],
    #     color="darkblue",
    #     length=1,
    #     normalize=False
    # )

    # Set plot limits and labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Cube Plot')

    ax.set_xlim3d(-3, 3)
    ax.set_ylim3d(-3, 3)
    ax.set_zlim3d(-1, 1)

    print(f"""Data:
        {center = }
        {rotation = }
        {point = }
        {R = }
    )""")

    plt.axis("equal")
    plt.pause(.1)

plt.show()
