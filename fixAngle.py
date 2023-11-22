import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation as R
import os
import sys
from time import sleep
from pytransform3d.rotations import plot_basis as pr
from pytransform3d.rotations import quaternion_from_matrix as qmp
import matplotlib.pyplot as plt
from pytransform3d.rotations import concatenate_quaternions as cq


path = os.getcwd()
sys.path.append(path)
from RobotArm import robot_control
from Laser import optoNCDT1402
from RaspberryPi import transistor


## Gets euler angles and quaterneons of a plane relative to another plane from 3 points.


robot = robot_control.connect_to_robot()
laser = optoNCDT1402.optoNCDT1402("/dev/ttyUSB0", 20)  # Serial port of the Raspberry
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
while not (point_zero_one == point_zero_two):
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

    ax1 = plt.figure().add_subplot(projection="3d")

    normalized_plane_normal = plane_normal / np.linalg.norm(plane_normal)
    ax1.quiver(
        0,
        0,
        0,
        normalized_plane_normal[0],
        normalized_plane_normal[1],
        normalized_plane_normal[2],
    )
    #plt.show()

    plane_basis = [
        vector_two,
        vector_one,
        normalized_plane_normal,
    ]

    dihedral_angle_x_cos = np.arccos(  ##Angle between two vectors
        np.dot(vector_two, reference_plane[2])
        / (np.linalg.norm(vector_two) * np.linalg.norm(reference_plane[2]))
    )

    dihedral_angle_y_cos = np.arccos(  ##Angle between two vectors
        np.dot(vector_one, reference_plane[2])
        / (np.linalg.norm(vector_one) * np.linalg.norm(reference_plane[2]))
    )
    dihedral_angle_z = np.arccos(
        np.dot(vector_one,reference_plane[0])
        /(np.linalg.norm(vector_one) * np.linalg.norm(reference_plane[0]))
    )

    y_angle = (np.pi / 2 - dihedral_angle_y_cos)/2
    x_angle = (dihedral_angle_x_cos - np.pi / 2)/2
    z_angle = (np.pi/2 - dihedral_angle_z)/2
    R_z = [
        [np.cos(z_angle),np.sin(z_angle),0],
        [-np.sin(z_angle),np.cos(z_angle),0],
        [0,0,1],
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
    R_zx = np.matmul(R_z,R_x)
    RotMat = np.matmul(R_zx,R_y)

    test_rotmat = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    ax = pr(R=test_rotmat)
    pr(ax=ax, R=RotMat)
    #plt.show()

    quaternions = qmp(RotMat)
    quaternions_temp = cq(quaternions_temp, quaternions)
    """quaternions_temp = []
    quaternions_temp.append(quaternions[3])
    for quats in quaternions[0:3]:
        quaternions_temp.append(quats)"""

    print(quaternions_temp)

    # reference_normal = normalized_plane_normal  # Sets the new reference normal to the previous computed normal
    # reference_plane = plane_basis

    quaternions_test = []
    for quats in quaternions_temp:
        quaternions_test.append(quats)
    quaternions_test.append(point_zero_one - point_zero_two)
    quaternions_to_save = pd.DataFrame(
        np.array([quaternions_test]),
        index=["Computed Quaternions : "],
        columns=["W", "X", "Y", "Z", "Difference in height"],
    )
    print(np.linalg.norm(quaternions_temp))
    filename = "testData\\quaternions" + str(i) + ".csv"
    quaternions_to_save.to_csv(filename)
    print(point_zero_one - point_zero_two)
    i = i + 1
