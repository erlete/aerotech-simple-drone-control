import matplotlib.pyplot as plt

from src.sdc.modules.core.vector import Rotator3D, Vector3D
from src.sdc.modules.geometry.drone import Drone

drone = Drone(
    Vector3D(0, 0, 0),
    Rotator3D(0, 0, 0)
)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

drone.plot(ax)
plt.show()
