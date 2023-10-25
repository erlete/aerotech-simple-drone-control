import matplotlib.pyplot as plt

from src.sdc.modules.core.vector import Rotator3D, Vector3D
from src.sdc.modules.geometry.ring import Ring1 as Ring

ring = Ring(
    position=Vector3D(1, 2, 3),
    rotation=Rotator3D(0, 0, 90),
    height=1,
    hole_radius=5,
    complexity=50
)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

ax.set_xlim3d(-10, 10)
ax.set_ylim3d(-10, 10)
ax.set_zlim3d(-10, 10)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

# plt.axis("equal")

Vector3D(0, 0, 0).plot(ax, ".", color="darkred", ms=25)

ring.plot(ax)

# Title, labels and legend:
ax.set_title("Drone track view")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.legend(
    [
        "Start",
        "End",
        "Rings"
    ]
)

# Axis planes background color:
ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

# Grid and axis views:
# ax.grid(False)  # TODO: Activate this after debugging
# ax.set_axis_off()  # TODO: Activate this after debugging
ax.set_facecolor((1.0, 1.0, 1.0, 0.0))

# Projection, aspect and axis scale:
ax.set_proj_type("ortho")
ax.set_box_aspect((1, 1, 1))
ax.set_autoscale_on(False)

# View distance and angle:
ax.view_init(azim=-135, elev=45)
ax.dist = 10


plt.show()
