"""Simulation API module.

This module combines all API resources to compose the Simulation API,
responsible for the execution, update and summary of the simulation.

Author:
    Paulo Sanchez (@erlete)
"""


import json
import os
from time import perf_counter as pc
from typing import List, Optional, Union

import matplotlib.pyplot as plt
import numpy as np

from ..core.gradient import ColorGradient
from ..core.vector import Rotator3D, Vector3D, distance3D
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
    DR = 4 * np.pi  # [rad/s]

    SUMMARY_FILE_PREFIX = "summary_"
    SUMMARY_DIR = "statistics"

    def __init__(self, tracks: List[Track]) -> None:
        """Initialize a SimulationAPI instance.

        Args:
            tracks (List[Track]): track list.
        """
        self._completed_statistics: List[TrackStatistics] = []
        self._statistics = [
            TrackStatistics(TrackAPI(track), self.DT)
            for track in tracks
        ]
        self.tracks = [TrackAPI(track) for track in tracks]  # Conversion.

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
            if not isinstance(track, TrackAPI):
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
        yaw: Union[int, float],
        pitch: Union[int, float],
        speed: Union[int, float]
    ) -> None:
        """Set drone target state.

        Args:
            yaw (Union[int, float]): target drone yaw in radians.
            pitch (Union[int, float]): target drone pitch in radians.
            speed (Union[int, float]): target drone speed in m/s.
        """
        if not isinstance(yaw, (int, float)):
            raise TypeError(
                "expected type (int, float) for"
                + f" {self.__class__.__name__}.set_drone_target_state yaw"
                + f" but got {type(yaw).__name__} instead"
            )

        if not isinstance(pitch, (int, float)):
            raise TypeError(
                "expected type (int, float) for"
                + f" {self.__class__.__name__}.set_drone_target_state pitch"
                + f" but got {type(pitch).__name__} instead"
            )

        if not isinstance(speed, (int, float)):
            raise TypeError(
                "expected type Union[int, float] for"
                + f" {self.__class__.__name__}.set_drone_target_state speed"
                + f" but got {type(speed).__name__} instead"
            )

        self._target_rotation = Rotator3D(
            np.rad2deg(yaw),
            np.rad2deg(pitch),
            0
        )
        self._target_speed = speed

    def update(
        self,
        plot: bool = True,
        dark_mode: bool = False,
        fullscreen: bool = True
    ) -> None:
        """Update drone state along the current track and plot environment.

        Args:
            plot (bool): whether to plot statistics after each track. Defaults
                to True.
            dark_mode (bool): whether to use dark mode for the plot. Defaults
                to False. Only used if plot is True.
            fullscreen (bool): whether to plot the figure in fullscreen mode.
                Defaults to True. Only used if plot is True.
        """
        self._current_timer += self.DT

        # Simulation endpoint conditions' definition for later use:
        c1 = self._current_timer >= self._current_track.timeout
        c2 = self._current_track.is_track_finished
        c3 = self._current_track.is_drone_stopped

        # On completed track finish condition:
        if c2 and c3:
            self._current_statistics.is_completed = True
            self._current_statistics.distance_to_end = distance3D(
                self._current_track.drone.position,
                self._current_track.track.end
            )

        # On each of the simulation finish conditions:
        if c1 or (c2 and c3):

            if plot:
                self.plot(dark_mode, fullscreen)

            # Save current statistics:
            self._completed_statistics.append(self._current_statistics)

            if self._tracks:
                self._current_track = self._tracks.pop(0)
                self._current_statistics = self._statistics.pop(0)
                self._current_timer = 0.0
            else:
                self._is_simulation_finished = True

            return

        # Rotation update:
        self._current_track.drone.rotation = Rotator3D(
            *[
                np.rad2deg(
                    min(cu_r + self.DR * self.DT, tg_r)
                    if cu_r < tg_r else
                    max(cu_r - self.DR * self.DT, tg_r)
                ) for cu_r, tg_r in zip(
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

        # Position update:
        rot = self._current_track.drone.rotation
        self._current_track.drone.position += (
            Vector3D(
                speed * self.DT * np.cos(rot.x) * np.cos(rot.y),
                speed * self.DT * np.sin(rot.x) * np.cos(rot.y),
                speed * self.DT * np.sin(rot.y)
            )
        )

        self._current_statistics.add_data(
            position=self._current_track.drone.position,
            rotation=self._current_track.drone.rotation,
            speed=self._current_track.drone.speed
        )

    def plot(self, dark_mode: bool, fullscreen: bool) -> None:
        """Plot simulation environment.

        Args:
            dark_mode (bool): whether to use dark mode for the plot.
            fullscreen (bool): whether to plot the figure in fullscreen mode.
        """
        times = np.arange(0, self._current_track.timeout, self.DT)
        speeds = [item[2] for item in self._current_statistics.data]
        rotations = [
            [item[1].x for item in self._current_statistics.data],
            [item[1].y for item in self._current_statistics.data],
            [item[1].z for item in self._current_statistics.data]
        ]

        # Figure and axes setup:
        plt.style.use("dark_background" if dark_mode else "fast")
        fig = plt.figure()
        ax1 = fig.add_subplot(121, projection="3d")
        ax2 = fig.add_subplot(422)
        ax3 = fig.add_subplot(424)
        ax4 = fig.add_subplot(426)
        ax5 = fig.add_subplot(428)

        # 2D axes configuration:
        axes = (ax2, ax3, ax4, ax5)
        labels = (
            "Speed [m/s]",
            "X rotation [rad]",
            "Y rotation [rad]",
            "Z rotation [rad]"
        )
        titles = (
            "Speed vs Time",
            "X rotation vs Time",
            "Y rotation vs Time",
            "Z rotation vs Time"
        )
        data = (speeds, *rotations)

        for ax, data_, title, label in zip(axes, data, titles, labels):
            ax.plot(times[:len(data_)], data_)
            ax.set_xlim(0, self._current_track.timeout)
            ax.set_title(titles[axes.index(ax)])
            ax.set_xlabel("Time [s]")
            ax.set_ylabel(label)
            ax.grid(True)

        ax2.set_ylim(self._current_track.drone.SPEED_RANGE)

        # 3D ax configuration:
        self._current_track._track.plot(ax1)
        positions = [
            [pos.x for pos in self._current_statistics.positions],
            [pos.y for pos in self._current_statistics.positions],
            [pos.z for pos in self._current_statistics.positions]
        ]
        gradient = ColorGradient("#dc143c", "#15b01a", len(positions[0]))
        for x, y, z, c in zip(*positions, gradient.steps):
            ax1.plot(x, y, z, "D", color=ColorGradient.rgb_to_hex(c), ms=4)

        ax1.set_title("3D Flight visualization")
        ax1.set_xlabel("X [m]")
        ax1.set_ylabel("Y [m]")
        ax1.set_zlabel("Z [m]")  # type: ignore

        # Figure configuration:
        plt.tight_layout()
        plt.get_current_fig_manager().window.state(  # type: ignore
            "zoomed" if fullscreen else "normal"
        )
        plt.show()

    def summary(self, save: bool = False) -> None:
        """Print a summary of the simulation.

        Args:
            save (bool): whether to save the summary to a file. Defaults to
                False.
        """
        header = f"{' Simulation summary ':=^80}"
        track = [
            f"""{' Track ' + str(i) + ' ':-^80}
    > Completed: {s.is_completed}
    > Distance to end: {s.distance_to_end:.5f} m
    > Max speed: {max(s.speeds):.5f} m/s
    > Min speed: {min(s.speeds):.5f} m/s
    > Average speed: {np.mean(s.speeds):.5f} m/s
""" for i, s in enumerate(self._completed_statistics, start=1)
        ]

        overall = f"""
{' Overall ':-^80}
    > Total tracks: {(t := len(self._completed_statistics))}
    > Completed tracks: {
        (c := len([s for s in self._completed_statistics if s.is_completed]))
    } ({c / t * 100:.2f}%)
    > Max speed: {
        max([max(s.speeds) for s in self._completed_statistics])
    :.5f} m/s
    > Min speed: {
        min([min(s.speeds) for s in self._completed_statistics])
    :.5f} m/s
    > Average speed: {
        np.mean([np.mean(s.speeds) for s in self._completed_statistics])
    :.5f} m/s
"""

        footer = "=" * 80

        print(f"{header}\n{''.join(track).strip()}{overall}{footer}")

        if save:
            self._save_summary()

    def _save_summary(self) -> None:
        """Save simulation summary to a file."""
        if not os.path.exists(self.SUMMARY_DIR):
            os.makedirs(self.SUMMARY_DIR)

        with open(
            f"{self.SUMMARY_DIR}/{self.SUMMARY_FILE_PREFIX}{int(pc())}.json",
            mode="w",
            encoding="utf-8"
        ) as fp:
            json.dump(
                {
                    "tracks": [
                        {
                            "is_completed": s.is_completed,
                            "distance_to_end": s.distance_to_end,
                            "positions": [
                                [position.x, position.y, position.z]
                                for position in s.positions
                            ],
                            "rotations": [
                                [rotation.x, rotation.y, rotation.z]
                                for rotation in s.rotations
                            ],
                            "speeds": s.speeds
                        } for s in self._completed_statistics
                    ],
                    "overall": {
                        "total_tracks": len(self._completed_statistics),
                        "completed_tracks": len(
                            [s for s in self._completed_statistics
                             if s.is_completed]
                        ),
                        "max_speed": max(
                            [max(s.speeds) for s in self._completed_statistics]
                        ),
                        "min_speed": min(
                            [min(s.speeds) for s in self._completed_statistics]
                        ),
                        "average_speed": np.mean([
                            np.mean(s.speeds)
                            for s in self._completed_statistics
                        ])
                    }
                },
                fp
            )
