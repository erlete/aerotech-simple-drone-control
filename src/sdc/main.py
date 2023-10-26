"""Main simulation module.

This module contains all simulation code. It imports the Simulation API, which
allows the user to control a Drone along a set of designed tracks.

Author:
    Paulo Sanchez (@erlete)
"""


from modules.api.simulation import SimulationAPI
from modules.core.vector import Rotator3D, Vector3D
from modules.environment.reader import TrackSequenceReader

TRACKS_DATABASE = "src/sdc/databases/tracks.json"


# Simulation API definition:
sim = SimulationAPI(TrackSequenceReader(TRACKS_DATABASE).track_sequence)

# Simulation mainloop:
while not sim.is_finished:

    """Drone element.

    This element represents the dynamic part of the simulation. It provides
    with several methods that allow the user to get information about the
    drone's state and control it.

    Attributes:
        position (Vector3D): current drone position.
        rotation (Rotator3D): current drone rotation.
        speed (float): current drone speed.
    """
    drone = sim.drone

    """Next waypoint data.

    This element provides information about the location (x, y, z) of the next
    waypoint of the track. It can either be a Vector3D or None if the end of
    the track has been reached.
    """
    next_wp = sim.next_waypoint

    # TODO: implement path planning and control logic here.
    #   Set target drone rotation using sim.set_drone_rotation(Rotator3D(...))
    #   Set target drone speed using sim.set_drone_speed(float(...))
    #   Note: you can remove this comment once you have implemented the logic.

    # Update simulation state:
    sim.update()

# Print simulation statistics summary:
sim.summary()
