from typing import Tuple, Union

import numpy as np

from ..core.vector import Rotator3D, Vector3D


class Ring:
    """Ring representation class.

    Attributes:
        position (Vector3D): ring position.
        rotation (Rotator3D): ring rotation.
        scale (Vector3D): ring scale.
        height (float): ring width.
        hole_radius (float): ring hole radius.
        complexity (int): ring geometry complexity.
        surface (Tuple[np.ndarray, np.ndarray, np.ndarray]): ring geometry
            surface.
    """

    def __init__(
        self,
        position: Vector3D = Vector3D(0, 0, 0),
        rotation: Rotator3D = Rotator3D(0, 0, 0),
        scale: Vector3D = Vector3D(1, 1, 1),
        height: Union[int, float] = 1,
        hole_radius: Union[int, float] = 5,
        complexity: int = 50
    ) -> None:
        """Initialize a Ring instance.

        Args:
            position (Vector3D, optional): ring position. Defaults to
                Vector3D(0, 0, 0).
            rotation (Rotator3D, optional): ring rotation. Defaults to
                Rotator3D(0, 0, 0).
            scale (Vector3D, optional): ring scale. Defaults to
                Vector3D(1, 1, 1).
            height (Union[int, float], optional): ring width. Defaults to 1.
            hole_radius (Union[int, float], optional): ring hole radius.
                Defaults to 5.
            complexity (int, optional): ring geometry complexity. Defaults to
                50.
        """
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.height = height
        self.hole_radius = hole_radius
        self.complexity = complexity

        self._compute_geometry()

    @property
    def position(self) -> Vector3D:
        """Get ring position.

        Returns:
            Vector3D: ring position.
        """
        return self._position

    @position.setter
    def position(self, value: Vector3D) -> None:
        """Set ring position.

        Args:
            value (Vector3D): ring position.
        """
        if not isinstance(value, Vector3D):
            raise TypeError(
                "expected type Vector3D for"
                + f" {self.__class__.__name__}.position but got"
                + f" {type(value).__name__} instead"
            )

        self._position = value

    @property
    def rotation(self) -> Rotator3D:
        """Get ring rotation.

        Returns:
            Rotator3D: ring rotation.
        """
        return self._rotation

    @rotation.setter
    def rotation(self, value: Rotator3D) -> None:
        """Set ring rotation.

        Args:
            value (Rotator3D): ring rotation.
        """
        if not isinstance(value, Rotator3D):
            raise TypeError(
                "expected type Rotator3D for"
                + f" {self.__class__.__name__}.rotation but got"
                + f" {type(value).__name__} instead"
            )

        self._rotation = value

    @property
    def scale(self) -> Vector3D:
        """Get ring scale.

        Returns:
            Vector3D: ring scale.
        """
        return self._scale

    @scale.setter
    def scale(self, value: Vector3D) -> None:
        """Set ring scale.

        Args:
            value (Vector3D): ring scale.
        """
        if not isinstance(value, Vector3D):
            raise TypeError(
                "expected type Vector3D for"
                + f" {self.__class__.__name__}.scale but got"
                + f" {type(value).__name__} instead"
            )

        self._scale = value

    @property
    def height(self) -> float:
        """Get ring height.

        Returns:
            float: ring height.
        """
        return self._height

    @height.setter
    def height(self, value: Union[int, float]) -> None:
        """Set ring height.

        Args:
            value (Union[int, float]): ring height.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(
                "expected type Union[int, float] for"
                + f" {self.__class__.__name__}.height but got"
                + f" {type(value).__name__} instead"
            )

        self._height = float(value)

    @property
    def hole_radius(self) -> float:
        """Get ring hole radius.

        Returns:
            float: ring hole radius.
        """
        return self._hole_radius

    @hole_radius.setter
    def hole_radius(self, value: Union[int, float]) -> None:
        """Set ring hole radius.

        Args:
            value (Union[int, float]): ring hole radius.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(
                "expected type Union[int, float] for"
                + f" {self.__class__.__name__}.hole_radius but got"
                + f" {type(value).__name__} instead"
            )

        self._hole_radius = float(value)

    @property
    def complexity(self) -> int:
        """Get ring geometry complexity.

        Returns:
            int: ring geometry complexity.
        """
        return self._complexity

    @complexity.setter
    def complexity(self, value: Union[int, float]) -> None:
        """Set ring geometry complexity.

        Args:
            value (Union[int, float]): ring geometry complexity.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(
                "expected type Union[int, float] for"
                + f" {self.__class__.__name__}.complexity but got"
                + f" {type(value).__name__} instead"
            )

        self._complexity = int(value)

    @property
    def surface(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Get ring geometry surface.

        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray]: ring geometry surface.
        """
        return self._surface

    def _compute_geometry(self) -> None:
        """Compute ring geometry.

        This method builds the ring geometry, scales it, rotates it and
        translates it to the correct position.
        """
        theta, phi = np.meshgrid(
            np.linspace(0, 2 * np.pi, self._complexity),  # type: ignore
            np.linspace(0, 2 * np.pi, self._complexity)  # type: ignore
        )

        x = (self._hole_radius + self._height * np.cos(theta)) * np.cos(phi)
        y = (self._hole_radius + self._height * np.cos(theta)) * np.sin(phi)
        z = self._height * np.sin(theta)

        azimuth, elevation, yaw = self._rotation

        # FIXME: turn this into a numpy matrix.
        x, y, z = np.cos(azimuth) * np.cos(elevation) * x + \
            (np.cos(azimuth) * np.sin(elevation) * np.sin(yaw) - np.sin(azimuth) * np.cos(yaw)) * y + \
            (np.cos(azimuth) * np.sin(elevation) * np.cos(yaw) + np.sin(azimuth) * np.sin(yaw)) * z, \
            np.sin(azimuth) * np.cos(elevation) * x + \
            (np.sin(azimuth) * np.sin(elevation) * np.sin(yaw) + np.cos(azimuth) * np.cos(yaw)) * y + \
            (np.sin(azimuth) * np.sin(elevation) * np.cos(yaw) - np.cos(azimuth) * np.sin(yaw)) * z, \
            -np.sin(elevation) * x + np.cos(elevation) * np.sin(yaw) * y + np.cos(elevation) * np.cos(yaw) * z

        x *= self._scale.x
        y *= self._scale.y
        z *= self._scale.z

        x += self._position.x
        y += self._position.y
        z += self._position.z

        self._surface = (x, y, z)

    def plot(self, ax, **kwargs) -> None:
        """Plot ring.

        Args:
            ax (Axes3D): ax to plot on.
        """
        kwargs_ = {
            "rstride": 5,
            "cstride": 5,
            "color": 'k',
            "edgecolors": 'w'
        }
        kwargs_.update(kwargs)

        ax.plot_surface(
            *self._surface,
            **kwargs_
        )

        self._position.plot(ax, ".", color=kwargs_["color"], ms=10)

    def __repr__(self) -> str:
        """Get short ring representation.

        Returns:
            str: short ring representation.
        """
        return f"<Ring at {self._position}>"

    def __str__(self) -> str:
        """Get long ring representation.

        Returns:
            str: long ring representation.
        """
        return f"""Ring(
    position={self._position},
    rotation={self._rotation},
    scale={self._scale},
    height={self._height},
    hole_radius={self._hole_radius},
    complexity={self._complexity}
)"""
