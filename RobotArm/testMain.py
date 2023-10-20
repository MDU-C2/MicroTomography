from RobotArm import generate_Scan_points_Cylinder
from Laser import optoNCDT1402
from time import sleep

from . import robot_Control


circle_radius = 60
z_stepsize = 10
max_depth = -70
azimuthPoints = 8
offset = -50

points = generate_Scan_points_Cylinder.generate_scan_points_cylinder(
    circle_radius, z_stepsize, max_depth, azimuthPoints, offset
)

"""laser = optoNCDT1402.optoNCDT1402("COM3")
laser_data = []

robot = robot_Control.connect_To_Robot()

robot_Control.set_Reference_Coordinate_System(robot, [0, 0, 755])


robot_Control.set_Robot_Tool(robot, 1)

robotSpeed = [75, 25, 50, 25]


robot_Control.set_Robot_Speed(robot, robotSpeed)

robot_Control.return_Robot_To_Start(robot)

for point in points:
    print(point)
    robot_Control.move_Robot_Linear(robot, point)
    sleep(1)
    print("Robot Coordinate: ", robot_Control.fetch_Robot_Coordinates(robot))
    laser.laserOn()
    if isinstance(laser.measure(), float):
        laser_data.append(laser.measure())
    laser.laserOff()
    print(laser_data)


robot_Control.return_Robot_To_Start(robot)

robot_Control.close_Connection(robot)
"""