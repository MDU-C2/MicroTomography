from RobotArm import robot_control, generate_scan_points
from Laser import optoNCDT1402
from time import sleep

# from tkinter import filedialog

import pandas as pd


circle_radius = 120
z_stepsize = 10
max_depth = -60
azimuthPoints = 16
offset = -60
elevationPoints = 10
zMin = -60

pointsCylinder = generate_scan_points.generate_scan_points_cylinder(
    circle_radius, z_stepsize, max_depth, azimuthPoints, offset
)

pointsSphere = generate_scan_points.generate_scan_points_halfsphere(
    circle_radius, azimuthPoints, elevationPoints, zMin, offset
)


robot = robot_control.robot_init(2)

robot_control.set_zone_use(robot, False)

for point in pointsCylinder:
    robot_control.move_robot_linear(robot, point)
    sleep(0.5)
    print("Robot Coordinate: ", robot_control.fetch_robot_coordinates(robot))

robot_control.return_robot_to_start(robot)

robot_control.close_connection(robot)
