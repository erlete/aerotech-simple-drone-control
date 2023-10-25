from typing import List


class ColorGradient:

    def __init__(self, initial_color, final_color, step_count):
        self.initial_color = initial_color
        self.final_color = final_color
        self.step_count = step_count

    @property
    def initial_color(self) -> str:
        """Get gradient initial color.

        Returns:
            str: gradient initial color.
        """
        return self._initial_color

    @initial_color.setter
    def initial_color(self, value: str) -> None:
        """Set gradient initial color.

        Args:
            value (str): gradient initial color.
        """
        if not isinstance(value, str):
            raise TypeError(
                "expected type str for"
                + f" {self.__class__.__name__}.initial_color but got"
                + f" {type(value).__name__} instead"
            )

        self._initial_color = value

    @property
    def final_color(self) -> str:
        """Get gradient final color.

        Returns:
            str: gradient final color.
        """
        return self._final_color

    @final_color.setter
    def final_color(self, value: str) -> None:
        """Set gradient final color.

        Args:
            value (str): gradient final color.
        """
        if not isinstance(value, str):
            raise TypeError(
                "expected type str for"
                + f" {self.__class__.__name__}.final_color but got"
                + f" {type(value).__name__} instead"
            )

        self._final_color = value

    @property
    def step_count(self) -> int:
        """Get gradient step count.

        Returns:
            int: gradient step count.
        """
        return self._step_count

    @step_count.setter
    def step_count(self, value: int) -> None:
        """Set gradient step count.

        Args:
            value (int): gradient step count.
        """
        if not isinstance(value, int):
            raise TypeError(
                "expected type int for"
                + f" {self.__class__.__name__}.step_count but got"
                + f" {type(value).__name__} instead"
            )

        self._step_count = value

    @property
    def steps(self) -> List[List[int]]:
        """Get gradient steps.

        Returns:
            List[List[int]]: gradient steps.
        """
        return self._compute_steps()

    @staticmethod
    def hex_to_rgb(hex_str: str) -> List[int]:
        """Convert a hex color string to RGB."""
        return [int(hex_str[i:i + 2], 16) for i in range(1, 6, 2)]

    def _compute_steps(self) -> List[List[int]]:
        """Compute gradient steps."""
        initial_rgb = self.hex_to_rgb(self.initial_color)
        final_rgb = self.hex_to_rgb(self.final_color)

        return [
            [
                int(
                    initial_rgb[i] + (final_rgb[i] - initial_rgb[i])
                    * step / self._step_count
                ) for i in range(3)
            ] for step in range(self._step_count)
        ]
