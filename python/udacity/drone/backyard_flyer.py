import time
from enum import Enum
import numpy as np
from udacidrone import Drone
from udacidrone.connection import MavlinkConnection
from udacidrone.messaging import MsgID

# create enum by creating a class
# that extends python's `Enum`


class Phases(Enum):
    MANUAL = 0
    ARMING = 1
    TAKEOFF = 2
    LANDING = 3
    DISARMING = 4
    WAYPOINTS = 5


class BackyardFlyer(Drone):

    def __init__(self, connection, waypoints=[]):
        super().__init__(connection)
        self.target_position = np.array([0.0, 0.0, 0.0])
        self.in_mission = True

        # initial state
        self.flight_phase = Phases.MANUAL

        self.waypoints = waypoints
        self.waypoints_reached = []

        # Register all your callbacks here.
        # `register_callback()` is inherited from `udacidrone.Drone`.
        # The callbacks will be triggered whenever
        # `udacidrone.messaging` changes.
        self.register_callback(MsgID.LOCAL_POSITION,
                               self.local_position_callback)
        self.register_callback(MsgID.LOCAL_VELOCITY,
                               self.velocity_callback)
        self.register_callback(MsgID.STATE,
                               self.state_callback)

    def waypoints_transition(self, cb):
        print("waypoints transition")

        time.sleep(3)
        self.flight_phase == Phases.WAYPOINTS

        altitude = self.target_position[2]
        heading = 0.0

        for point in self.waypoints:
            if len(point) < 3:
                point.append(altitude)
            if len(point) < 4:
                point.append(heading)
            self.cmd_position(*point)
            self.waypoints_reached.append(point)
            print("- flying to point {} of {}: {}".format(
                len(self.waypoints_reached), len(self.waypoints), point))
            time.sleep(5)

        # run callback
        print("{} waypoints reached. executing callback..".format(
            len(self.waypoints_reached)))
        cb()

    def local_position_callback(self):
        if self.flight_phase == Phases.TAKEOFF:
            if len(self.waypoints_reached) < len(self.waypoints):
                self.waypoints_transition(self.landing_transition)
                return
            # coordinate conversion
            altitude = -1.0 * self.local_position[2]

            # check if altitude is within 95% of target
            if altitude > 0.95 * self.target_position[2]:
                self.landing_transition()

    def _home_distance(self):
        return (abs(self.global_position[0] - self.global_home[0]),
                abs(self.global_position[1] - self.global_home[1]))

    def _around_home(self):
        east, north = self._home_distance()
        return east < 0.01 and north < 0.01

    def _safe_to_land(self):
        return abs(self.local_position[2]) < 0.01

    def velocity_callback(self):
        print("velocity_callback. phase:", self.flight_phase)

        print("- altitude:", self.local_position[2])
        print("- safe to land:", self._safe_to_land())
        print("- home distance:", self._home_distance())
        print("- around home:", self._around_home())

        if self.flight_phase == Phases.LANDING:
            if not self._around_home():
                print("going home..")
                print("- home distance:", self._home_distance())
                print('- global pos', self.global_position[0:2])
                print('- global home', self.global_home[0:2])

                self.cmd_position(0., 0., 3., 0.)
                time.sleep(3)

            if not self._safe_to_land():
                print("landing..")
                time.sleep(3)
                self.cmd_position(0., 0., 0., 0.)
                time.sleep(3)

            self.disarming_transition()

    def state_callback(self):
        if not self.in_mission:
            return
        if self.flight_phase == Phases.MANUAL:
            self.arming_transition()
        elif self.flight_phase == Phases.ARMING:
            if self.armed:
                self.takeoff_transition()
        elif self.flight_phase == Phases.DISARMING:
            if not self.armed:
                self.manual_transition()

    def arming_transition(self):
        print("arming transition")
        self.take_control()
        self.arm()

        # set the current location to be the home position
        print("setting home position..")
        self.set_home_position(self.global_position[0],
                               self.global_position[1],
                               self.global_position[2])

        self.flight_phase = Phases.ARMING

    def takeoff_transition(self):
        print("takeoff transition")
        target_altitude = 3.0
        self.target_position[2] = target_altitude
        self.takeoff(target_altitude)
        self.flight_phase = Phases.TAKEOFF

    def landing_transition(self):
        print("landing transition")
        self.land()
        self.flight_phase = Phases.LANDING

    def disarming_transition(self):
        print("disarm transition")
        self.disarm()
        self.flight_phase = Phases.DISARMING

    def manual_transition(self):
        print("manual transition")
        self.release_control()
        self.stop()
        self.in_mission = False
        self.flight_phase = Phases.MANUAL

    def start(self):
        self.start_log("Logs", "NavLog.txt")
        print("starting connection")
        super().start()
        self.stop_log()


if __name__ == "__main__":
    conn = MavlinkConnection('tcp:127.0.0.1:5760',
                             threaded=False,
                             PX4=False)

    square_waypoints = [
        [2.0, 0.0],     # fly forward by 5 points
        [2.0, -2.0],    # fly to left by 5 points
        [0.0, -2.0],    # fly backward by 5 points
        [0.0, 0.0]]     # back to home position
    drone = BackyardFlyer(conn, square_waypoints)
    time.sleep(2)
    drone.start()
