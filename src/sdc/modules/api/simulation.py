"""Simulation API module.

This module combines all API resources to compose the Simulation API,
responsible for the execution, update and summary of the simulation.

Author:
    Paulo Sanchez (@erlete)
"""


from typing import List, Optional

from ..core.vector import Rotator3D, Vector3D
from ..environment.track import Track
from ..geometry.drone import Drone
from .drone import DroneAPI
from .track import TrackAPI


class SimulationAPI:

    def __init__(self, tracks: List[Track]) -> None:
        # Internal attribute initialization:
        self._is_finished = False
        self._next_waypoint = None
        self._drone = DroneAPI(Drone(Vector3D(0, 0, 0), Rotator3D(0, 0, 0)))

        self.tracks = [TrackAPI(self._drone, track) for track in tracks]

    @property
    def is_finished(self) -> bool:
        """Returns whether the simulation is finished.

        Returns:
            bool: True if the simulation is finished, False otherwise.
        """
        return self._is_finished

    @property
    def drone(self) -> DroneAPI:
        """Returns the drone element.

        Returns:
            DroneAPI: drone element.
        """
        return self._drone

    @property
    def next_waypoint(self) -> Optional[Vector3D]:
        """Returns the next waypoint data.

        Returns:
            Optional[Vector3D]: next waypoint data.
        """
        return self._next_waypoint
