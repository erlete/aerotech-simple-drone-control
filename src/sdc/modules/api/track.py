"""Track API module.

Author:
    Paulo Sanchez (@erlete)
"""


from typing import List, Optional

from ..core.vector import Rotator3D, Vector3D, distance3D
from ..environment.track import Track
from .drone import DroneAPI


class TrackAPI:
    """Track API class.

    This class represents a kinematic version of a track, implementing the
    geometry of the track, adding a drone to it and providing information about
    next waypoint, remaining ones, whether the track is finished and whether
    the drone is stopped.

    Attributes:
        track (Track): track.
        drone (DroneAPI): drone.
        waypoints (List[Vector3D]): track waypoints.
        next_waypoint (Optional[Vector3D]): next waypoint data.
        remaining_waypoints (int): remaining waypoints in the track.
        is_track_finished (bool): whether the track is finished.
        is_drone_stopped (bool): whether the drone is stopped.
        REACHED_THRESHOLD (float): reached waypoint threshold in m.
    """

    REACHED_THRESHOLD = 4  # [m]

    def __init__(self, track: Track) -> None:
        """Initialize a TrackAPI instance.

        Args:
            track (Track): track.
        """
        self.track = track

        # Internal attributes:
        self._drone = DroneAPI(track.start, Rotator3D())

    @property
    def track(self) -> Track:
        """Get track.

        Returns:
            Track: track.
        """
        return self._track

    @track.setter
    def track(self, value: Track) -> None:
        """Set track.

        Args:
            value (Track): track.
        """
        if not isinstance(value, Track):
            raise TypeError(
                "expected type Track for"
                + f" {self.__class__.__name__}.track but got"
                + f" {type(value).__name__} instead"
            )

        # Internal attributes reset:
        self._waypoints = [*[ring.position for ring in value.rings], value.end]
        self._next_waypoint: Optional[Vector3D] = self._waypoints.pop(0)
        self._is_track_finished = self._is_drone_stopped = False

        self._track = value

    @property
    def drone(self) -> DroneAPI:
        """Get drone.

        Returns:
            DroneAPI: drone.
        """
        return self._drone

    @property
    def waypoints(self) -> List[Vector3D]:
        """Get track waypoints.

        Returns:
            List[Vector3D]: track waypoints.
        """
        return self._waypoints

    @property
    def next_waypoint(self) -> Optional[Vector3D]:
        """Update and return next waypoint data.

        Returns:
            Optional[Vector3D]: next waypoint data or None if the track is
                finished.
        """
        self._eval_reached_waypoint()
        return self._next_waypoint

    @property
    def remaining_waypoints(self) -> int:
        """Get remaining waypoints in the track (including current one).

        Returns:
            int: remaining waypoints in the track (including current one).
        """
        return len(self._waypoints) + 1  # Compensation for current waypoint.

    @property
    def is_track_finished(self) -> bool:
        """Check whether the track is finished.

        Returns:
            bool: True if the track is finished, False otherwise.
        """
        return self._is_track_finished

    @property
    def is_drone_stopped(self) -> bool:
        """Check whether the drone is stopped.

        Returns:
            bool: True if the drone is stopped, False otherwise.
        """
        return self._is_track_finished and self._drone.speed == 0

    def _eval_reached_waypoint(self) -> None:
        """Evaluate whether the drone has reached the next waypoint.

        This method is responsible for updating the next waypoint data if the
        drone has reached the current one. It also updates the finished track
        flag if the end of the last waypoint has been reached.
        """
        # Prevent evaluation if the track is finished:
        if self._is_track_finished:
            return

        distance = distance3D(
            self._drone.position,
            self._next_waypoint  # type: ignore
        )

        if distance <= self.REACHED_THRESHOLD:
            if self._waypoints:  # If there are any waypoints left:
                self._next_waypoint = self._waypoints.pop(0)
            else:
                self._next_waypoint = None
                self._is_track_finished = True
