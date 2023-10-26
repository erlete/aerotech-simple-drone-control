"""Control API module.

Author:
    Paulo Sanchez (@erlete)
"""

from typing import Union

from ..geometry.drone import Drone


class DroneAPI:
    """Drone API class.

    This class represents a kinematic drone model, implementing the geometry
    of the drone and adding a speed attribute to it.

    Attributes:
        drone (Drone): drone.
        speed (float): drone speed in m/s.
        SPEED_RANGE (Tuple[int, int]): allowed drone speed range in m/s.
    """

    SPEED_RANGE = (0, 20)  # [m/s]

    def __init__(self, drone: Drone, speed: Union[int, float] = 0) -> None:
        """Initialize a DroneAPI instance.

        Args:
            drone (Drone): drone.
            speed (Union[int, float], optional): drone speed in m/s. Defaults
                to 0.
        """
        self.drone = drone
        self.speed = speed

    @property
    def drone(self) -> Drone:
        """Get drone.

        Returns:
            Drone: drone.
        """
        return self._drone

    @drone.setter
    def drone(self, value: Drone) -> None:
        """Set drone.

        Args:
            value (Drone): drone.
        """
        if not isinstance(value, Drone):
            raise TypeError(
                "expected type Drone for"
                + f" {self.__class__.__name__}.drone but got"
                + f" {type(value).__name__} instead"
            )

        self._drone = value

    @property
    def speed(self) -> float:
        """Get drone speed.

        Returns:
            float: drone speed.
        """
        return self._speed

    @speed.setter
    def speed(self, value: Union[int, float]) -> None:
        """Set drone speed.

        Args:
            value (Union[int, float]): drone speed.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(
                "expected type Union[int, float] for"
                + f" {self.__class__.__name__}.speed but got"
                + f" {type(value).__name__} instead"
            )

        # Limited speed setting:
        self._speed = float(
            max(self.SPEED_RANGE[0], min(value, self.SPEED_RANGE[1]))
        )

    def plot(self, ax) -> None:
        """Plot drone.

        Args:
            ax (Axes3D): ax to plot drone on.
        """
        self._drone.plot(ax)
