import sys
import os

pathname = os.getcwd()

sys.path.append(r"/home/mwi/Repositories/MicroTomography")


from RobotArm import robot_control
from Laser.optoNCDT1402 import optoNCDT1402

from RaspberryPi import transistor


laser = optoNCDT1402(noMeasurements=50)

transistor.init()
robot = robot_control.connect_to_robot()
robot_control.set_reference_coordinate_system(
    robot, [[0.6, -7.5, 759.24], [9.99954527e-01, 9.41712207e-03, 1.50357889e-03, 9.45543129e-06]]
)
robot_control.set_robot_tool(robot, 1)
robot_control.set_robot_speed(robot, [75, 25, 50, 25])



robot_control.move_robot_linear(robot, [[0, 0, -110], [1, 0, 0, 0]])

transistor.laserON()