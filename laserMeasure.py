import sys
import os

pathname = os.getcwd()

sys.path.append("../Microtomography")

from RobotArm import robot_control, generate_scan_points
from Laser.optoNCDT1402 import optoNCDT1402
from RaspberryPi import transistor
from time import sleep
import numpy as np

laser = optoNCDT1402()  # Serial port of the Raspberry Pi
laser_data = []

transistor.init()
robot = robot_control.robot_init(1)

points = [[[0, y, -130], [1, 0, 0, 0]] for y in np.arange(-5, 5+1e-10, 1)]
print(points)

# Visit all points and scan the laser at the given points
for point in points:
    robot_control.move_robot_linear(robot, point)
    sleep(1)

    transistor.laserON()

    laser_point = laser.measure()
    if isinstance(laser_point, float):
        laser_data.append(laser_point)
        '''laser_data.append(
            generate_scan_points.transform_laser_distance(point, laser_point)
        )'''
    transistor.laserOff()

robot_control.close_connection(robot)
print(laser_data)
