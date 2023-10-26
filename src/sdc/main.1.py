from sdc.modules.api.control import FlightAPI
from sdc.modules.core.vector import Rotator3D, Vector3D
from sdc.modules.environment.reader import TrackSequenceReader
from sdc.modules.geometry.drone import Drone

reader = TrackSequenceReader("src/sdc/databases/tracks.json")
tracks = reader.track_sequence

fa = FlightAPI(Drone(Vector3D(0, 0, 0), Rotator3D(0, 0, 0)), tracks)
