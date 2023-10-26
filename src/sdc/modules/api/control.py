"""Control API module.

Author:
    Paulo Sanchez (@erlete)
"""

from typing import List, Optional

from ..environment.track import Track
from ..geometry.drone import Drone


class DroneAPI:

    def __init__(self, drone, track):
        self.drone = drone
        self.track = track


class TrackAPI:

    def __init__(self, track: Track) -> None:
        self.track = track

        self._is_finished = False
        self._elapsed = None
        self._distance_to_end = None

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

        self._track = value



class FlightAPI:

    def __init__(self, drone: Drone, tracks: List[Track]) -> None:
        self.drone = drone
        self.tracks = tracks

        self._set_new_track()

    @property
    def drone(self) -> Drone:
        """Get track drone.

        Returns:
            Drone: track drone.
        """
        return self._drone

    @drone.setter
    def drone(self, value: Drone) -> None:
        """Set track drone.

        Args:
            value (Drone): track drone.
        """
        if not isinstance(value, Drone):
            raise TypeError(
                "expected type Drone for"
                + f" {self.__class__.__name__}.drone but got"
                + f" {type(value).__name__} instead"
            )

        self._drone = value

    @property
    def tracks(self) -> List[Track]:
        """Get track list.

        Returns:
            List[Track]: track list.
        """
        return self._tracks

    @tracks.setter
    def tracks(self, value: List[Track]) -> None:
        """Set track list.

        Args:
            value (List[Track]): track list.
        """
        if not isinstance(value, list):
            raise TypeError(
                "expected type List[Track] for"
                + f" {self.__class__.__name__}.tracks but got"
                + f" {type(value).__name__} instead"
            )

        if not value:
            raise ValueError(
                f"expected non-empty list for"
                + f" {self.__class__.__name__}.tracks"
            )

        for track in value:
            if not isinstance(track, Track):
                raise TypeError(
                    f"expected type Track for item {track} in"
                    + f" {self.__class__.__name__}.tracks but got"
                    + f" {type(value).__name__} instead"
                )

        self._tracks = value

    @property
    def current_track(self) -> Optional[Track]:
        """Get current track.

        Returns:
            Track: current track.
        """
        return self._current_track

    def _set_new_track(self) -> None:
        if len(self._tracks) >= 1:
            self._current_track = self._tracks.pop(0)
            self._has_next_track = True
        else:
            self._current_track = self._tracks.pop(0)
            self._has_next_track = False
