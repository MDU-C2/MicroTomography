import sys
import os

pathname = os.getcwd()

sys.path.append(r"C:\Users\jjn17015\Documents\MicroTomography")


from RobotArm.generate_scan_points import generate_scan_points_cylinder

from RobotArm import robot_control
from time import sleep
from Laser.optoNCDT1402 import optoNCDT1402

from RaspberryPi import transistor
import numpy as np
from pytransform3d.rotations import (
    quaternion_from_axis_angle,
    concatenate_quaternions,
)

laser = optoNCDT1402()

transistor.init()
robot = robot_control.robot_init(1)

radius = 150
step = 10
depth = -110
offset = -110
azi = 16

q1 = [1, 0, 0, 0]
WOBJ_POS = [-5.27669, -4.89651, 764.097]


max_laser = 100
min_laser = 0
best = 10

while best < 0.3:
    robot_control.set_reference_coordinate_system(robot, [WOBJ_POS, q1])

    points = generate_scan_points_cylinder(radius, step, depth, azi, offset)

    laser_data = []

    for point in points:
        alteredPoint = [point[0], [1, 0, 0, 0]]

        robot_control.move_robot_linear(robot, alteredPoint)
        sleep(4)

        transistor.laserON()

        laser_point = laser.measure()
        if isinstance(laser_point, float):
            laser_data.append([point[0][0], point[0][1], point[0][2], laser_point])
        transistor.laserOff()

    laser_data = np.array(laser_data)

    max_value = max(laser_data[:, -1])
    min_value = min(laser_data[:, -1])
    e = max_value - min_value

    i_max = np.where(laser_data[:, -1] == max_value)
    i_min = np.where(laser_data[:, -1] == min_value)

    if len(i_max) > 1:
        i_max = i_max[0]

    if len(i_min) > 1:
        i_min = i_min[0]

    data_max = laser_data[i_max]
    data_min = laser_data[i_min]

    dp = np.sqrt(np.sum((data_max[0][:2] - data_min[0][:2]) ** 2))

    angle = np.arctan(e / dp)

    v1 = data_max[0][:-1] - data_min[0][:-1]
    v1 = v1 / np.linalg.norm(v1)
    v2 = np.array([0, 0, 1])
    normal = np.cross(v2, v1)

    q = quaternion_from_axis_angle(np.append(normal, angle / 4))
    q1 = concatenate_quaternions(q1=q1, q2=q)

    diff = max_laser - min_laser
    print(f"The difference between max and min: {diff}")
    print(f"With quaternions: {q1}")
    if diff < best:
        best = diff

print("")
print(f"The best difference between max and min: {best}")
print(f"With quaternions: {q1}")
