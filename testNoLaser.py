from RobotArm import robot_Control, generate_Scan_points_Cylinder
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

pointsCylinder = generate_Scan_points_Cylinder.generate_scan_points_cylinder(
    circle_radius, z_stepsize, max_depth, azimuthPoints, offset
)

pointsSphere = generate_Scan_points_Cylinder.generate_scan_points_halfSphere(
    circle_radius, azimuthPoints, elevationPoints, zMin, offset
)


robot = robot_Control.connect_To_Robot()

robot_Control.set_Reference_Coordinate_System(robot, [43.37, 38.92, 754.16])


robot_Control.set_Robot_Tool(robot, 1)

robotSpeed = [75, 25, 50, 25]


robot_Control.set_Robot_Speed(robot, robotSpeed)

robot_Control.return_Robot_To_Start(robot)

for point in pointsCylinder:
    robot_Control.move_Robot_Linear(robot, point)
    sleep(0.5)
    print("Robot Coordinate: ", robot_Control.fetch_Robot_Coordinates(robot))

robot_Control.return_Robot_To_Start(robot)

robot_Control.close_Connection(robot)
