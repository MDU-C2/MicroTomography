"""
Michael Dawson-Haggerty.

abb.py: contains classes and support functions which interact with an ABB Robot running our software stack (RAPID code module SERVER)


For functions which require targets (XYZ positions with quaternion orientation),
targets can be passed as [[XYZ], [Quats]] OR [XYZ, Quats]

"""

import socket
import json
import time
import inspect
from collections import deque
import logging

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class Robot:
    def __init__(self, ip="192.168.0.50", port_motion=5000, port_logger=5001):
        self.delay = 0.08

        self.connect_motion((ip, port_motion))
        self.ip = ip
        self.port_motion = port_motion
        self.set_units("millimeters", "degrees")
        self.set_tool()
        self.set_workobject()
        self.set_speed()

    def connect_motion(self, remote):
        log.info("Attempting to connect to robot motion server at %s", str(remote))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(10)
        self.sock.connect(remote)
        self.sock.settimeout(None)
        log.info("Connected to robot motion server at %s", str(remote))

    def connect_logger(self, remote, maxlen=None):
        self.pose = deque(maxlen=maxlen)
        self.joints = deque(maxlen=maxlen)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(remote)
        s.setblocking(1)
        try:
            while True:
                data = map(float, s.recv(4096).split())
                if int(data[1]) == 0:
                    self.pose.append([data[2:5], data[5:]])
        finally:
            s.shutdown(socket.SHUT_RDWR)

    def set_units(self, linear, angular):
        units_l = {"millimeters": 1.0, "meters": 1000.0, "inches": 25.4}
        units_a = {"degrees": 1.0, "radians": 57.2957795}
        self.scale_linear = units_l[linear]
        self.scale_angle = units_a[angular]

    def set_cartesian(self, pose):
        """
        Executes a move immediately from the current pose,
        to 'pose', with units of millimeters.
        """
        msg = "01 " + self.format_pose(pose)
        return self.send(msg)

    def set_joints(self, joints):
        """
        Executes a move immediately, from current joint angles,
        to 'joints', in degrees.
        """
        if len(joints) != 7:
            return False
        msg = "02 "
        for joint in joints:
            msg += format(joint * self.scale_angle, "+08.2f") + " "
        msg += "#"
        return self.send(msg)

    def get_cartesian(self):
        """
        Returns the current pose of the robot, in millimeters
        """
        msg = "03 #"
        data = self.send(msg).split()
        r = [float(s) for s in data]
        return [r[2:5], r[5:9]]

    def get_joints(self):
        """
        Returns the current angles of the robots joints, in degrees.
        """
        msg = "04 #"
        data = self.send(msg).split()
        return [float(s) / self.scale_angle for s in data[2:9]]

    def set_tool(self, tool=[[0, 0, 0], [1, 0, 0, 0]]):
        """
        Sets the tool centerpoint (TCP) of the robot.
        When you command a cartesian move,
        it aligns the TCP frame with the requested frame.

        Offsets are from tool0, which is defined at the intersection of the
        tool flange center axis and the flange face.
        """
        msg = "06 " + self.format_pose(tool)
        self.send(msg)
        self.tool = tool

    def set_workobject(self, work_obj=[[0, 0, 0], [1, 0, 0, 0]]):
        """
        The workobject is a local coordinate frame you can define on the robot,
        then subsequent cartesian moves will be in this coordinate frame.
        """
        msg = "07 " + self.format_pose(work_obj)
        self.send(msg)

    def set_speed(self, speed=[100, 50, 50, 50]):
        """
        speed: [robot TCP linear speed (mm/s), TCP orientation speed (deg/s),
                external axis linear, external axis orientation]
        """

        if len(speed) != 4:
            return False
        msg = "08 "
        msg += format(speed[0], "+08.1f") + " "
        msg += format(speed[1], "+08.2f") + " "
        msg += format(speed[2], "+08.1f") + " "
        msg += format(speed[3], "+08.2f") + " #"
        self.send(msg)

    def change_current_tool(self, tool):
        """
        Changes the current TCP in use
        """
        msg = "12 "
        msg += format(tool, "+08.2f") + " #"
        self.send(msg)

    def use_zone_traverse(self, zone_traverse):
        """
        Set if zone traversement should be used or not

        zone_traverse = 0: No zone traversement enabled

        zone_traverse = 1: Zone traversement enabled
        """
        msg = "13 "
        msg += format(zone_traverse, "+08.2f") + " #"
        self.send(msg)

    def send(self, message, wait_for_response=True):
        """
        Send a formatted message to the robot socket.
        if wait_for_response, we wait for the response and return it
        """
        caller = inspect.stack()[1][3]
        log.debug("%-14s sending: %s", caller, message)
        self.sock.sendto(message.encode(), (self.ip, self.port_motion))
        time.sleep(self.delay)
        if not wait_for_response:
            return
        data = self.sock.recv(4096)
        log.debug("%-14s recieved: %s", caller, data)
        return data

    def format_pose(self, pose):
        pose = check_coordinates(pose)
        msg = ""
        for cartesian in pose[0]:
            msg += format(cartesian * self.scale_linear, "+08.1f") + " "
        for quaternion in pose[1]:
            msg += format(quaternion, "+08.5f") + " "
        msg += "#"
        return msg

    def close(self):
        self.send("99 #", False)
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        log.info("Disconnected from ABB robot.")

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()


def check_coordinates(coordinates):
    if (
        (len(coordinates) == 2)
        and (len(coordinates[0]) == 3)
        and (len(coordinates[1]) == 4)
    ):
        return coordinates
    elif len(coordinates) == 7:
        return [coordinates[0:3], coordinates[3:7]]
    log.warn("Recieved malformed coordinate: %s", str(coordinates))
    raise NameError("Malformed coordinate!")


if __name__ == "__main__":
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)-7s (%(filename)s:%(lineno)3s) %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )
    handler_stream = logging.StreamHandler()
    handler_stream.setFormatter(formatter)
    handler_stream.setLevel(logging.DEBUG)
    log = logging.getLogger("abb")
    log.setLevel(logging.DEBUG)
    log.addHandler(handler_stream)
