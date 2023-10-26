from ..environment.track import Track
from .drone import DroneAPI


class TrackAPI:

    def __init__(self, drone, track):
        self.drone = drone
        self.track = track


    def _set_new_checkpoint(self):
        self._checkpoints = self._checkpoints[1:]

    @property
    def next_checkpoint(self):
        return self._checkpoints[0] if self._checkpoints else None
    # next checkpoint retrieval
