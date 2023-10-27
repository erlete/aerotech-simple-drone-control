"""Simulation API module.

This module combines all API resources to compose the Simulation API,
responsible for the execution, update and summary of the simulation.

Author:
    Paulo Sanchez (@erlete)
"""


from typing import List, Optional, Union

import numpy as np

from ..core.vector import Rotator3D, Vector3D
from ..environment.track import Track
from .drone import DroneAPI
from .statistics import TrackStatistics
from .track import TrackAPI


class SimulationAPI:
    """Simulation API class.

    This class represents a simulation that implements all kinematic variants
    of the simulation elements, such as the drone and the track. It provides
    with several methods that allow the user to get information about the
    simulation's state and control it.

    Attributes:
        tracks (List[TrackAPI]): track list.
        drone (DroneAPI): drone element.
        next_waypoint (Optional[Vector3D]): next waypoint data.
        remaining_waypoints (int): remaining waypoints in the track.
        is_simulation_finished (bool): whether the simulation is finished.
        DT (float): simulation time step in seconds.
        DV (float): simulation speed step in m/s.
        DR (float): simulation rotation step in rad/s.
    """

    DT = 0.1  # [s]
    DV = 10  # [m/s]
    DR = np.pi/4  # [rad/s]

    def __init__(self, tracks: List[Track]) -> None:
        """Initialize a SimulationAPI instance.

        Args:
            tracks (List[Track]): track list.
        """
        self.tracks = [TrackAPI(track) for track in tracks]  # Conversion.
        self._statistics = [
            TrackStatistics(track, self.DT)
            for track in tracks
        ]

    @property
    def tracks(self) -> List[TrackAPI]:
        """Get track list.

        Returns:
            List[TrackAPI]: track list.
        """
        return self._tracks

    @tracks.setter
    def tracks(self, value: List[TrackAPI]) -> None:
        """Set track list.

        Args:
            value (List[TrackAPI]): track list.
        """
        if not isinstance(value, list):
            raise TypeError(
                "expected type List[Track] for"
                + f" {self.__class__.__name__}.tracks but got"
                + f" {type(value).__name__} instead"
            )

        if not value:
            raise ValueError(
                f"{self.__class__.__name__}.tracks cannot be empty"
            )

        for i, track in enumerate(value):
            if not isinstance(track, Track):
                raise TypeError(
                    "expected type Track for"
                    + f" {self.__class__.__name__}.tracks but got"
                    + f" {type(track).__name__} from item at index {i} instead"
                )

        self._tracks = value

        # Internal attributes reset:
        self._is_simulation_finished = False
        self._current_track = self._tracks.pop(0)
        self._current_statistics = self._statistics.pop(0)
        self._current_timer = 0.0
        self._target_rotation = Rotator3D()
        self._target_speed = 0.0

    @property
    def drone(self) -> DroneAPI:
        """Returns the drone element.

        Returns:
            DroneAPI: drone element.
        """
        return self._current_track.drone

    @property
    def next_waypoint(self) -> Optional[Vector3D]:
        """Returns the next waypoint data.

        Returns:
            Optional[Vector3D]: next waypoint data.
        """
        return self._current_track.next_waypoint

    @property
    def remaining_waypoints(self) -> int:
        """Returns the remaining waypoints in the track.

        Returns:
            int: remaining waypoints in the track.
        """
        return self._current_track.remaining_waypoints

    @property
    def is_simulation_finished(self) -> bool:
        """Returns whether the simulation is finished.

        Returns:
            bool: True if the simulation is finished, False otherwise.
        """
        return self._is_simulation_finished

    def set_drone_target_state(
        self,
        rotation: Rotator3D,
        speed: Union[int, float]
    ) -> None:
        """Set drone target state.

        Args:
            rotation (Rotator3D): target drone rotation.
            speed (Union[int, float]): target drone speed.
        """
        if not isinstance(rotation, Rotator3D):
            raise TypeError(
                "expected type Rotator3D for"
                + f" {self.__class__.__name__}.set_drone_target_state"
                + f" but got {type(rotation).__name__} instead"
            )

        if not isinstance(speed, (int, float)):
            raise TypeError(
                "expected type Union[int, float] for"
                + f" {self.__class__.__name__}.set_drone_target_state"
                + f" but got {type(speed).__name__} instead"
            )

        self._target_rotation = rotation
        self._target_speed = speed

    def update(self) -> None:
        """Update drone state along the current track and plot environment."""
        self._current_timer += self.DT

        # Track timeout handling:
        if self._current_timer >= self._current_track.timeout:
            if self._tracks:
                self._current_track = self._tracks.pop(0)
                self._current_statistics = self._statistics.pop(0)
            else:
                self._is_simulation_finished = True

            return

        # Track finish handling:
        if (
            self._current_track.is_track_finished
            and self._current_track.is_drone_stopped
        ):
            if self._tracks:
                self._current_track = self._tracks.pop(0)
                self._current_statistics = self._statistics.pop(0)
            else:
                self._is_simulation_finished = True

            return

        # Rotation update:
        self._current_track.drone.rotation = Rotator3D(
            *[
                min(cu_r + self.DR * self.DT, tg_r)
                if cu_r < tg_r else
                max(cu_r - self.DR * self.DT, tg_r)
                for cu_r, tg_r in zip(
                    self._current_track.drone.rotation,
                    self._target_rotation
                )
            ]
        )

        # Speed update:
        speed = self._current_track.drone.speed
        self._current_track.drone.speed = (
            min(speed + self.DV * self.DT, self._target_speed)
            if self._target_speed >= speed else
            max(speed - self.DV * self.DT, self._target_speed)
        )

        # TODO: Add displacement update here.

        self._current_statistics.add_data(
            position=self._current_track.drone.position,
            rotation=self._current_track.drone.rotation,
            speed=self._current_track.drone.speed
        )

    def summary(self) -> None:
        pass
