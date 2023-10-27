"""Track statistics generation module.

Author:
    Paulo Sanchez (@erlete)
"""


from typing import List, Tuple, Union

from ..api.track import TrackAPI
from ..core.vector import Rotator3D, Vector3D
from ..geometry.track import Track


class TrackStatistics:

    def __init__(
        self,
        track: Union[Track, TrackAPI],
        timestep: Union[int, float]
    ) -> None:
        """Initialize a TrackStatistics instance.

        Args:
            track (Union[Track, TrackAPI]): statistics track.
            timestep (Union[int, float]): statistics timestep.
        """
        self.timestep = timestep
        self._waypoints = track.waypoints

        # Automatically generated attributes:
        self._is_completed = False
        self._distance_to_end = 0
        self._data = []  # type: ignore

    @property
    def timestep(self) -> Union[int, float]:
        """Get statistics timestep.

        Returns:
            Union[int, float]: statistics timestep.
        """
        return self._timestep

    @timestep.setter
    def timestep(self, value: Union[int, float]) -> None:
        """Set statistics timestep.

        Args:
            value (Union[int, float]): statistics timestep.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(
                "expected type Union[int, float] for"
                + f" {self.__class__.__name__}.timestep but got"
                + f" {type(value).__name__} instead"
            )

        self._timestep = value

    @property
    def waypoints(self) -> List[Vector3D]:
        """Get track waypoints.

        Returns:
            List[Vector3D]: track waypoints.
        """
        return self._waypoints

    @property
    def is_completed(self) -> bool:
        """Get track completion status.

        Returns:
            bool: track completion status.
        """
        return self._is_completed

    @is_completed.setter
    def is_completed(self, value: bool) -> None:
        """Set track completion status.

        Args:
            value (bool): track completion status.
        """
        if not isinstance(value, bool):
            raise TypeError(
                "expected type bool for"
                + f" {self.__class__.__name__}.is_completed but got"
                + f" {type(value).__name__} instead"
            )

        self._is_completed = value

    @property
    def distance_to_end(self) -> float:
        """Get drone distance to track end.

        Returns:
            float: drone distance to track end.
        """
        return self._distance_to_end

    @distance_to_end.setter
    def distance_to_end(self, value: Union[int, float]) -> None:
        """Set drone distance to track end.

        Args:
            value (Union[int, float]): drone distance to track end.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(
                "expected type Union[int, float] for"
                + f" {self.__class__.__name__}.distance_to_end but got"
                + f" {type(value).__name__} instead"
            )

        self._distance_to_end = float(value)

    @property
    def data(self) -> List[Tuple[Vector3D, Rotator3D, Union[int, float]]]:
        """Get drone position, rotation and speed data at each timestep.

        Returns:
            List[Tuple[Vector3D, Rotator3D, Union[int, float]]]: position,
                rotation and speed of the drone at each timestep.
        """
        return self._data

    def add_data(
        self,
        position: Vector3D,
        rotation: Rotator3D,
        speed: Union[int, float]
    ) -> None:
        """Add drone position, rotation and speed data.

        Args:
            position (Vector3D): drone position.
            rotation (Rotator3D): drone rotation.
            speed (Union[int, float]): drone speed.
        """
        if not isinstance(position, Vector3D):
            raise TypeError(
                "expected type Vector3D for"
                + f" {self.__class__.__name__}.add_data but got"
                + f" {type(position).__name__} instead"
            )

        if not isinstance(rotation, Rotator3D):
            raise TypeError(
                "expected type Rotator3D for"
                + f" {self.__class__.__name__}.add_data but got"
                + f" {type(rotation).__name__} instead"
            )

        if not isinstance(speed, (int, float)):
            raise TypeError(
                "expected type Union[int, float] for"
                + f" {self.__class__.__name__}.add_data but got"
                + f" {type(speed).__name__} instead"
            )

        self._data.append((position, rotation, speed))
