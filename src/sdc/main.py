"""Main simulation module.

This module contains all simulation code. It imports the Simulation API, which
allows the user to control a Drone along a set of designed tracks. The API
automatically handles track switching, so the information it provides is always
related to the current track.

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
while not sim.is_simulation_finished:

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

    The next_waypoint provides information about the location (x, y, z) of the
    next waypoint of the track. It can either be a Vector3D or None if the end
    of the track has been reached. On the other hand, the `remaining` element
    provides information on how many waypoints are left in the track. If it
    reaches 0, the track is finished.
    """
    next_waypoint, remaining = sim.next_waypoint, sim.remaining_waypoints

    # TODO: implement path planning and control logic here.

    # Update drone state (modify this with your own logic output values):
    sim.set_drone_target_state(
        rotation=Rotator3D(0, 0, 0),
        speed=0
    )

    # Update simulation state:
    sim.update()

# Print simulation statistics summary:
sim.summary()
