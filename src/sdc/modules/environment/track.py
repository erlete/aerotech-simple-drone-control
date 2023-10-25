"""Track utilities container module.

Author:
    Paulo Sanchez (@erlete)
"""


from typing import List

from ..core.vector import Vector3D
from ..geometry.ring import Ring


class Track:
    """Track representation class.

    This class is used to represent a track composed of a start point, an end
    point and a sequence of rings.

    Attributes:
        start (Vector3D): track start.
        end (Vector3D): track end.
        rings (List[Ring]): track rings.
    """

    def __init__(
        self,
        start: Vector3D,
        end: Vector3D,
        rings: List[Ring]
    ) -> None:
        """Initialize a Track instance.

        Args:
            start (Vector3D): track start.
            end (Vector3D): track end.
            rings (List[Ring]): track rings.
        """
        self.start = start
        self.end = end
        self.rings = rings

    @property
    def start(self) -> Vector3D:
        """Get track start.

        Returns:
            Vector3D: track start.
        """
        return self._start

    @start.setter
    def start(self, value: Vector3D) -> None:
        """Set track start.

        Args:
            value (Vector3D): track start.
        """
        if not isinstance(value, Vector3D):
            raise TypeError(
                "expected type Vector3D for"
                + f" {self.__class__.__name__}.start but got"
                + f" {type(value).__name__} instead"
            )

        self._start = value

    @property
    def end(self) -> Vector3D:
        """Get track end.

        Returns:
            Vector3D: track end.
        """
        return self._end

    @end.setter
    def end(self, value: Vector3D) -> None:
        """Set track end.

        Args:
            value (Vector3D): track end.
        """
        if not isinstance(value, Vector3D):
            raise TypeError(
                "expected type Vector3D for"
                + f" {self.__class__.__name__}.end but got"
                + f" {type(value).__name__} instead"
            )

        self._end = value

    @property
    def rings(self) -> List[Ring]:
        """Get track rings.

        Returns:
            List[Ring]: track rings.
        """
        return self._rings

    @rings.setter
    def rings(self, value: List[Ring]) -> None:
        """Set track rings.

        Args:
            value (List[Ring]): track rings.
        """
        if not isinstance(value, list):
            raise TypeError(
                "expected type List[Ring] for"
                + f" {self.__class__.__name__}.rings but got"
                + f" {type(value).__name__} instead"
            )

        for element in value:
            if not isinstance(element, Ring):
                raise TypeError(
                    f"expected Ring, got {type(element).__name__}"
                    + f"on element {element} instead"
                )

        self._rings = value

    def plot(self, ax, **kwargs) -> None:
        """Plot track.

        Args:
            ax (Axes3D): 3D axis.
            **kwargs: plot arguments.
        """
        self.start.plot(ax, "+", color="darkred", **kwargs)
        self.end.plot(ax, "P", color="darkgreen", **kwargs)

        for ring in self.rings:
            ring.plot(ax, color="darkorange", **kwargs)

    def __repr__(self) -> str:
        """Get short track representation.

        Returns:
            str: short track representation.
        """
        return f"<Track with {len(self._rings)} rings>"

    def __str__(self) -> str:
        """Get long track representation.

        Returns:
            str: long track representation.
        """
        return (
            f"Track from {self._start} to {self._end} with"
            + f" rings: {self._rings}"
        )

    def __len__(self) -> int:
        """Get track length.

        Returns:
            int: track length.
        """
        return len(self._rings) + 2  # Start and end points compensation.
