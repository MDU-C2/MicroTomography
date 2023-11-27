#!/bin/python3

from Laser.optoNCDT1402 import optoNCDT1402
from RobotArm import generate_scan_points
from RobotArm import robot_control
from RaspberryPi import transistor
from time import sleep

import numpy as np


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

    laser = optoNCDT1402("/dev/ttyUSB0", 1)  # Serial port of the Raspberry Pi
    laser_data = []

    transistor.init()
    robot = robot_control.robot_init(1)
    robot_control.set_zone_use(robot, True)
    robot_control.move_robot_linear(robot, points[0])
    robot_control.set_zone_use(robot, False)

    # Visit all points and scan the laser at the given points
    for point in points:
        robot_control.move_robot_linear(robot, point)
        while not (
            np.round(robot.get_cartesian()[0], 1) == np.round(point[0], 1)
        ).all():
            continue
        sleep(1)

        transistor.laserON()

        laser_point = laser.measure()
        if isinstance(laser_point, float):
            laser_data.append(
                generate_scan_points.transform_laser_distance(point, laser_point)
            )
        transistor.laserOff()

    robot_control.set_zone_use(robot, True)
    robot_control.close_connection(robot)
    return laser_data


def find_nipple(z_offset, distance, side_len):
    points = generate_scan_points.generate_points_in_square_plane(
        z_offset, distance, side_len
    )
    min_laser_point = 1000
    points_of_min_laser_point = []

    laser = optoNCDT1402("/dev/ttyUSB0")  # Serial port of the Raspberry Pi
    transistor.init()
    robot = robot_control.robot_init(1)

    robot_control.set_zone_use(robot, 0)
    laser_data = []

    for point in points:
        robot_control.move_robot_linear(robot, [point, [1, 0, 0, 0]])

        # while not (np.round(robot.get_cartesian()[0], 1) == point).all():
        # print(np.round(robot.get_cartesian()[0], 1))
        # continue
        sleep(1)
        transistor.laserON()
        laser_point = laser.measure()
        print(laser_point)
        if isinstance(laser_point, float):
            if laser_point < min_laser_point:
                min_laser_point = laser_point
                points_of_min_laser_point = point
            laser_data.append(
                generate_scan_points.transform_laser_distance(
                    [point, [1, 0, 0, 0]], laser_point
                )
            )

        transistor.laserOff()

    robot_control.return_robot_to_start(robot)
    robot_control.close_connection(robot)

    return points_of_min_laser_point, z_offset + min_laser_point, laser_data


def find_lowest_point(z_offset=-130):
    laser = optoNCDT1402("/dev/ttyUSB0", 10)  # Serial port of the Raspberry Pi
    transistor.init()
    robot = robot_control.robot_init(1)
    temp_laser_data = [0, 0, 0, 0, 0]

    tol = 0.5

    initial_point = [0, 0, 0]
    q = [1, 0, 0, 0]

    inc = [10, 5, 1, 0.5, 0.3, 0.1, 0.05]

    center_point = np.add(initial_point, [0, 0, z_offset])
    x_pos_point = np.add(center_point, [10, 0, 0])
    x_neg_point = np.add(center_point, [-10, 0, 0])
    y_pos_point = np.add(center_point, [0, 10, 0])
    y_neg_point = np.add(center_point, [0, -10, 0])

    lowest_point = [10, 10, 10]
    for i in inc:
        was_center = False
        while not was_center:
            robot_control.move_robot_linear(robot, [center_point, q])
            while not (
                np.isclose(robot.get_cartesian()[0], center_point, rtol=tol)
            ).all():
                continue
            sleep(2)
            transistor.laserON()
            temp_laser_data[0] = laser.measure()
            transistor.laserOff()

            robot_control.move_robot_linear(robot, [x_pos_point, q])
            while not (
                np.isclose(robot.get_cartesian()[0], x_pos_point, rtol=tol)
            ).all():
                continue
            sleep(2)
            transistor.laserON()
            temp_laser_data[1] = laser.measure()
            transistor.laserOff()

            robot_control.move_robot_linear(robot, [x_neg_point, q])
            while not (
                np.isclose(robot.get_cartesian()[0], x_neg_point, rtol=tol)
            ).all():
                continue
            sleep(2)
            transistor.laserON()
            temp_laser_data[2] = laser.measure()
            transistor.laserOff()

            robot_control.move_robot_linear(robot, [y_pos_point, q])
            while not (
                np.isclose(robot.get_cartesian()[0], y_pos_point, rtol=tol)
            ).all():
                continue
            sleep(2)
            transistor.laserON()
            temp_laser_data[3] = laser.measure()
            transistor.laserOff()

            robot_control.move_robot_linear(robot, [y_neg_point, q])
            while not (
                np.isclose(robot.get_cartesian()[0], y_neg_point, rtol=tol)
            ).all():
                continue
            sleep(2)
            transistor.laserON()
            temp_laser_data[4] = laser.measure()
            transistor.laserOff()

            if min(temp_laser_data) == temp_laser_data[0]:
                was_center = True
                lowest_point = center_point
            if min(temp_laser_data) == temp_laser_data[1]:
                lowest_point = x_pos_point
                center_point = x_pos_point
            if min(temp_laser_data) == temp_laser_data[2]:
                lowest_point = x_neg_point
                center_point = x_neg_point
            if min(temp_laser_data) == temp_laser_data[3]:
                lowest_point = y_pos_point
                center_point = y_pos_point
            if min(temp_laser_data) == temp_laser_data[4]:
                lowest_point = y_neg_point
                center_point = y_neg_point

            x_pos_point = np.add(center_point, [i, 0, 0])
            x_neg_point = np.add(center_point, [-i, 0, 0])
            y_pos_point = np.add(center_point, [0, i, 0])
            y_neg_point = np.add(center_point, [0, -i, 0])

    print(np.add(lowest_point, [0, 0, temp_laser_data[0]]))
    return np.add(lowest_point, [0, 0, temp_laser_data[0]])
