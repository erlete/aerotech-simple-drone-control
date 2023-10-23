"""Vector utilities container module.

This module contains all utilities related to vector generation and
manipulation operations.

Author:
    Paulo Sanchez (@erlete)
"""


from __future__ import annotations

import math
from typing import Any, Iterator, Union

import numpy as np


class Vector3D:
    """3D vector representation class.

    This class represents a vector in the 3D space. It can also be used to
    represent coordinates in a cartesian coordinate system.

    Attributes:
        x (float): X component of the vector.
        y (float): Y component of the vector.
        z (float): Z component of the vector.
    """

    def __init__(
        self,
        x: Union[int, float],
        y: Union[int, float],
        z: Union[int, float]
    ) -> None:
        """Initialize a Vector3D instance.

        Args:
            x (Union[int, float]): X component of the vector.
            y (Union[int, float]): Y component of the vector.
            z (Union[int, float]): Z component of the vector.
        """
        self.x = x
        self.y = y
        self.z = z

    @property
    def x(self) -> float:
        """Get X component of the vector.

        Returns:
            float: X component of the vector.
        """
        return self._x

    @x.setter
    def x(self, value: Union[int, float]) -> None:
        """Set X component of the vector.

        Args:
            value (Union[int, float]): X component of the vector.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(
                "expected type Union[int, float] for"
                + f" {self.__class__.__name__}.x but got"
                + f" {type(value).__name__} instead"
            )

        self._x = float(value)

    @property
    def y(self) -> float:
        """Get Y component of the vector.

        Returns:
            float: Y component of the vector.
        """
        return self._y

    @y.setter
    def y(self, value: Union[int, float]) -> None:
        """Set Y component of the vector.

        Args:
            value (Union[int, float]): Y component of the vector.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(
                "expected type Union[int, float] for"
                + f" {self.__class__.__name__}.y but got"
                + f" {type(value).__name__} instead"
            )

        self._y = float(value)

    @property
    def z(self) -> float:
        """Get Z component of the vector.

        Returns:
            float: Z component of the vector.
        """
        return self._z

    @z.setter
    def z(self, value: Union[int, float]) -> None:
        """Set Z component of the vector.

        Args:
            value (Union[int, float]): Z component of the vector.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(
                "expected type Union[int, float] for"
                + f" {self.__class__.__name__}.z but got"
                + f" {type(value).__name__} instead"
            )

        self._z = float(value)

    def plot(self, ax, *args, **kwargs) -> None:
        """Plot the vector.

        Args:
            ax (Axes3D): axes to plot the vector on.
        """
        ax.plot(*[[c, c] for c in self], *args, **kwargs)

    def __add__(self, other: Vector3D) -> Vector3D:
        """Add two vectors.

        Args:
            other (Vector3D): vector to add.

        Returns:
            Vector3D: resulting vector.
        """
        return Vector3D(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __sub__(self, other: Vector3D) -> Vector3D:
        """Subtract two vectors.

        Args:
            other (Vector3D): vector to subtract.

        Returns:
            Vector3D: resulting vector.
        """
        return Vector3D(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def __mul__(self, other: Union[int, float]) -> Vector3D:
        """Multiply a vector by a scalar.

        Args:
            other (Union[int, float]): scalar to multiply by.

        Returns:
            Vector3D: resulting vector.
        """
        if not isinstance(other, (int, float)):
            raise TypeError("only scalars are supported for multiplication")

        return Vector3D(
            self.x * other,
            self.y * other,
            self.z * other
        )

    def __rmul__(self, other: Union[int, float]) -> Vector3D:
        """Multiply a vector by a scalar.

        Args:
            other (Union[int, float]): scalar to multiply by.

        Returns:
            Vector3D: resulting vector.
        """
        if not isinstance(other, (int, float)):
            raise TypeError("only scalars are supported for multiplication")

        return Vector3D(
            self.x * other,
            self.y * other,
            self.z * other
        )

    def __truediv__(self, other: Union[int, float]) -> Vector3D:
        """Divide a vector by a scalar (float division).

        Args:
            other (Union[int, float]): scalar to divide by.

        Returns:
            Vector3D: resulting vector.
        """
        if not isinstance(other, (int, float)):
            raise TypeError("only scalars are supported for division")

        return Vector3D(
            self.x / other,
            self.y / other,
            self.z / other
        )

    def __floordiv__(self, other: Union[int, float]) -> Vector3D:
        """Divide a vector by a scalar (integer division).

        Args:
            other (Union[int, float]): scalar to divide by.

        Returns:
            Vector3D: resulting vector.
        """
        if not isinstance(other, (int, float)):
            raise TypeError("only scalars are supported for division")

        return Vector3D(
            self.x // other,
            self.y // other,
            self.z // other
        )

    def __mod__(self, other: Union[int, float]) -> Vector3D:
        """Get the remainder of a vector division by a scalar.

        Args:
            other (Union[int, float]): scalar to divide by.

        Returns:
            Vector3D: resulting vector.
        """
        if not isinstance(other, (int, float)):
            raise TypeError("only scalars are supported for modulo")

        return Vector3D(
            self.x % other,
            self.y % other,
            self.z % other
        )

    def __pow__(self, other: Union[int, float]) -> Vector3D:
        """Get the power of a vector.

        Args:
            other (Union[int, float]): scalar to raise to.

        Returns:
            Vector3D: resulting vector.
        """
        if not isinstance(other, (int, float)):
            raise TypeError("only scalars are supported for exponentiation")

        return Vector3D(
            self.x ** other,
            self.y ** other,
            self.z ** other
        )

    def __abs__(self) -> Vector3D:
        """Get the absolute value of a vector.

        Returns:
            Vector3D: resulting vector.
        """
        return Vector3D(
            abs(self.x),
            abs(self.y),
            abs(self.z)
        )

    def __neg__(self) -> Vector3D:
        """Get the negation of a vector.

        Returns:
            Vector3D: resulting vector.
        """
        return Vector3D(
            -self.x,
            -self.y,
            -self.z
        )

    def __pos__(self) -> Vector3D:
        """Get the positive value of a vector.

        Returns:
            Vector3D: resulting vector.
        """
        return Vector3D(
            +self.x,
            +self.y,
            +self.z
        )

    def __round__(self, n: int = 0) -> Vector3D:
        """Round a vector.

        Args:
            n (int, optional): number of decimals to round to. Defaults to 0.

        Returns:
            Vector3D: resulting vector.
        """
        return Vector3D(
            round(self.x, n),
            round(self.y, n),
            round(self.z, n)
        )

    def __floor__(self) -> Vector3D:
        """Get the floor of a vector.

        Returns:
            Vector3D: resulting vector.
        """
        return Vector3D(
            math.floor(self.x),
            math.floor(self.y),
            math.floor(self.z)
        )

    def __ceil__(self) -> Vector3D:
        """Get the ceiling of a vector.

        Returns:
            Vector3D: resulting vector.
        """
        return Vector3D(
            math.ceil(self.x),
            math.ceil(self.y),
            math.ceil(self.z)
        )

    def __trunc__(self) -> Vector3D:
        """Get the truncated value of a vector.

        Returns:
            Vector3D: resulting vector.
        """
        return Vector3D(
            math.trunc(self.x),
            math.trunc(self.y),
            math.trunc(self.z)
        )

    def __eq__(self, other: Any) -> bool:
        """Check if two vectors are equal.

        Args:
            other (Any): vector to compare to.

        Returns:
            bool: whether the two vectors are equal to another.
        """
        return (
            self.x == other.x
            and self.y == other.y
            and self.z == other.z
        )

    def __ne__(self, other: Any) -> bool:
        """Check if two vectors are not equal.

        Args:
            other (Any): vector to compare to.

        Returns:
            bool: whether the two vectors are not equal to another.
        """
        return (
            self.x != other.x
            or self.y != other.y
            or self.z != other.z
        )

    def __lt__(self, other: Any) -> bool:
        """Check if a vector is less than another one.

        Args:
            other (Any): vector to compare to.

        Returns:
            bool: whether the vector is less than another one.
        """
        raise NotImplementedError("< operation not supported for Vector3D")

    def __le__(self, other: Any) -> bool:
        """Check if a vector is less than or equal to another one.

        Args:
            other (Any): vector to compare to.

        Returns:
            bool: whether the vector is less than or equal to another one.
        """
        raise NotImplementedError("<= operation not supported for Vector3D")

    def __gt__(self, other: Any) -> bool:
        """Check if a vector is greater than another one.

        Args:
            other (Any): vector to compare to.

        Returns:
            bool: whether the vector is greater than another one.
        """
        raise NotImplementedError("> operation not supported for Vector3D")

    def __ge__(self, other: Any) -> bool:
        """Check if a vector is greater than or equal to another one.

        Args:
            other (Any): vector to compare to.

        Returns:
            bool: whether the vector is greater than or equal to another one.
        """
        raise NotImplementedError(">= operation not supported for Vector3D")

    def __bool__(self) -> bool:
        """Check if a vector is truthy.

        Returns:
            bool: whether the vector is truthy or not.
        """
        return bool(self.x or self.y or self.z)

    def __len__(self) -> int:
        """Get the length of a vector.

        Returns:
            int: length of the vector.
        """
        return 3

    def __iter__(self) -> Iterator:
        """Get an iterator for the vector.

        Returns:
            Iterator: iterator for the vector.
        """
        return iter((self.x, self.y, self.z))

    def __repr__(self) -> str:
        """Get the raw representation of the vector.

        Returns:
            str: raw representation of the vector.
        """
        return f"Vector3D({self.x}, {self.y}, {self.z})"

    def __str__(self) -> str:
        """Get the string representation of the vector.

        Returns:
            str: string representation of the vector.
        """
        return f"({self.x}, {self.y}, {self.z})"


class Rotator3D(Vector3D):
    """3D rotation representation class.

    This class represents a rotation in the 3D space. It can also be used to
    represent rotations in a cartesian coordinate system.

    Attributes:
        x (float): X rotation (degrees).
        y (float): Y rotation (degrees).
        z (float): Z rotation (degrees).
    """

    def __init__(
        self,
        x: Union[int, float],
        y: Union[int, float],
        z: Union[int, float]
    ) -> None:
        """Initialize a Rotator3D instance.

        Args:
            x (Union[int, float]): X rotation (degrees).
            y (Union[int, float]): Y rotation (degrees).
            z (Union[int, float]): Z rotation (degrees).
        """
        self.x = np.deg2rad(x)
        self.y = np.deg2rad(y)
        self.z = np.deg2rad(z)
