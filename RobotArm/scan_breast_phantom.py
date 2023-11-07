#!/bin/python3

from Laser.optoNCDT1402 import optoNCDT1402
from RobotArm import generate_scan_points, robot_Control
from RaspberryPi import transistor
from time import sleep


# Function for scanning points in either cylinder form or halfsphere form
def scan_points(*args):
    """
    Parameters
    ----------
    Cylinder form input: radius, z_stepsize, z_min, azimuth_points, z_offset and laser_angle

    Halsphere form input: radius, azimuth_points, elevation_points, z_min and z_offset

    """

    if len(args) == 6:
        points = generate_scan_points.generate_scan_points_cylinder(
            args[0], args[1], args[2], args[3], args[4], args[5]
        )
    elif len(args) == 5:
        points = generate_scan_points.generate_scan_points_halfsphere(
            args[0], args[1], args[2], args[3], args[4]
        )

    laser = optoNCDT1402("/dev/ttyUSB0")  # Serial port of the Raspberry Pi
    laser_data = []

    transistor.init()
    robot = robot_control.robot_init(1)

    # Visit all points and scan the laser at the given points
    for point in points:
        robot_control.move_robot_linear(robot, point)
        sleep(0.5)

        laser_point = laser.measure()
        if isinstance(laser_point, float):
            laser_data.append(
                generate_scan_points.transform_laser_distance(point, laser_point)
            )
        transistor.laserOff()

    robot_control.close_connection(robot)
    return laser_data
