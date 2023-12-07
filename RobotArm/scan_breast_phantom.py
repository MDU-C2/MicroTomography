#!/bin/python3
import sys
import os

path = os.getcwd()
sys.path.append(path)

from Laser.optoNCDT1402 import optoNCDT1402
from RobotArm import generate_scan_points
from RobotArm import robot_control
from RaspberryPi import transistor
from time import sleep

import numpy as np

import os
import sys
from pytransform3d.rotations import plot_basis as pr
from pytransform3d.rotations import quaternion_from_matrix as qmp
from pytransform3d.rotations import concatenate_quaternions as cq

from zvb.titi_bakonkadonk_brest_8008 import *


# Function for scanning points in either cylinder form or halfsphere form
def scan_points(quaternion, *args):
    """
    Parameters
    ----------
    quaternion: the quaternions for the work plane

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
    robot = robot_control.robot_init(1, quaternion)
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
        sleep(0.1)

        transistor.laserON()

        laser_point = laser.measure()
        if isinstance(laser_point, float):
            laser_data.append(
                generate_scan_points.transform_laser_distance(point, laser_point)
            )
        transistor.laserOff()

    transistor.close()
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

    robot_control.set_zone_use(robot, False)
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

    transistor.close()
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


def calibration():
    ## Gets euler angles and quaterneons of a plane relative to another plane from 3 points.
    robot = robot_control.connect_to_robot()
    laser = optoNCDT1402("/dev/ttyUSB0", 20)  # Serial port of the Raspberry3
    transistor.init()
    robot_control.set_reference_coordinate_system(
        robot, [[-5.27669, -4.89651, 764.097], [1, 0, 0, 0]]
    )
    robot_control.set_robot_tool(robot, 1)

    quaternions_tool = [1, 0, 0, 0]
    quaternions_temp = [1, 0, 0, 0]
    reference_plane = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    point_zero_one = 1
    point_zero_two = 2

    i = 0
    robot_control.set_zone_use(robot, False)

    while not (abs(point_zero_one - point_zero_two) < 1.0) or i < 3:
        print(f"Calibration number {i}")
        i = i + 1

        robot_control.return_robot_to_start(robot)
        print(quaternions_temp)
        robot_control.set_reference_coordinate_system(
            robot, [[-205.27669, -4.89651, 764.097], quaternions_temp]
        )

        points = [
            [[0, 0, -110], quaternions_tool],
            [[0, 200, -110], quaternions_tool],
            [[400, 0, -110], quaternions_tool],
        ]

        scanned_distance = []

        for point in points:
            robot_control.move_robot_linear(robot, point)
            sleep(2)
            transistor.laserON()
            laser_point = laser.measure()
            if isinstance(laser_point, float):
                scanned_distance.append(laser_point)
                print(laser_point)
            transistor.laserOff()

        scanned_points = [
            [0, 0, scanned_distance[0]],
            [0, 200, scanned_distance[1]],
            [400, 0, scanned_distance[2]],
        ]

        point_zero = scanned_points[0]
        point_zero_one = np.max(scanned_distance)
        point_zero_two = np.min(scanned_distance)
        vector_one = np.subtract(scanned_points[1], point_zero)
        vector_two = np.subtract(scanned_points[2], point_zero)
        vector_one = vector_one / np.linalg.norm(vector_one)
        vector_two = vector_two / np.linalg.norm(vector_two)
        plane_normal = np.cross(vector_two, vector_one)

        dihedral_angle_x_cos = np.arccos(  ##Angle between two vectors
            np.dot(vector_two, reference_plane[2])
            / (np.linalg.norm(vector_two) * np.linalg.norm(reference_plane[2]))
        )

        dihedral_angle_y_cos = np.arccos(  ##Angle between two vectors
            np.dot(vector_one, reference_plane[2])
            / (np.linalg.norm(vector_one) * np.linalg.norm(reference_plane[2]))
        )
        dihedral_angle_z = np.arccos(
            np.dot(vector_one, reference_plane[0])
            / (np.linalg.norm(vector_one) * np.linalg.norm(reference_plane[0]))
        )

        y_angle = (np.pi / 2 - dihedral_angle_y_cos) / 2
        x_angle = (dihedral_angle_x_cos - np.pi / 2) / 2
        z_angle = (np.pi / 2 - dihedral_angle_z) / 2
        R_z = [
            [np.cos(z_angle), np.sin(z_angle), 0],
            [-np.sin(z_angle), np.cos(z_angle), 0],
            [0, 0, 1],
        ]
        R_y = [
            [np.cos(x_angle), 0, np.sin(x_angle)],
            [0, 1, 0],
            [-np.sin(x_angle), 0, np.cos(x_angle)],
        ]
        R_x = [
            [1, 0, 0],
            [0, np.cos(y_angle), -np.sin(y_angle)],
            [0, np.sin(y_angle), np.cos(y_angle)],
        ]
        R_zx = np.matmul(R_z, R_x)
        RotMat = np.matmul(R_zx, R_y)

        test_rotmat = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        ax = pr(R=test_rotmat)
        pr(ax=ax, R=RotMat)

        quaternions = qmp(RotMat)
        quaternions_temp = cq(quaternions_temp, quaternions)

    robot_control.set_zone_use(robot, True)
    robot_control.close_connection(robot)
    return quaternions_temp


def microMoveForRobot(buttonNumber, mesh, surfacepoint, distance, quaternions):
    # increase or decrease values
    if buttonNumber == 1:  # X_up
        surfacepoint[0] = surfacepoint[0] + 10.0
    elif buttonNumber == 2:  # X_down
        surfacepoint[0] = surfacepoint[0] - 10.0
    elif buttonNumber == 3:  # Y_up
        surfacepoint[1] = surfacepoint[1] + 10.0
    elif buttonNumber == 4:  # Y_down
        surfacepoint[1] = surfacepoint[1] - 10.0
    elif buttonNumber == 5:  # Z_up
        surfacepoint[2] = surfacepoint[2] + 10.0
    elif buttonNumber == 6:  # Z_down
        surfacepoint[2] = surfacepoint[2] - 0.0

    Newpoint = [surfacepoint]

    # move robot using the move list funtion and get antenna position
    antenna_points, antenna_q = mw_micromovement(mesh, Newpoint, distance, quaternions)

    return antenna_points, antenna_q, surfacepoint
