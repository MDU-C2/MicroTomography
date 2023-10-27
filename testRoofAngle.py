from RobotArm import robot_Control, generate_Scan_points_Cylinder
from Laser import optoNCDT1402
from RaspberryPi import transistor
from time import sleep

robot = robot_Control.connect_To_Robot()

# robot_Control.set_Reference_Coordinate_System(robot, [0.6, -3.85, 755])

# When arm pointing down (x positive) (30, -30) quat: 0.707, 0.0, 0.707, 0.0
# When arm pointing up (x negative) (-30, 30) quat: 0.0, 0.707, 0.0, -0.707
# When arm pointing left (y negative) (-30, -30) quat: 0.0, -0.707, -0.0, 0.707

# 45 degree angle neg x, neg y (-45, 0) quat: 0.271, 0.653, 0.271, -0.653


# robot.set_calibration()

robot_Control.set_Robot_Tool(robot, 1)

robotSpeed = [75, 25, 50, 25]


robot_Control.set_Robot_Speed(robot, robotSpeed)

laser = optoNCDT1402.optoNCDT1402("/dev/ttyUSB0")  # Serial port of the Raspberry
transistor.init()
transistor.laserOff()


# robot_Control.return_Robot_To_Start(robot)

# robot.set_external_axis(0)
robot.set_joints([0, -135, 55, 0, 105, 4, 0])

robot.set_cartesian([[-258.27, 46.99, 650], [1, 0, 0, 0]])
sleep(2)

joints = robot.get_joints()
print(joints)
external_joint = robot.get_external_axis()
print(external_joint)


for angle in [-135, -45, 45, 135]:
    joints[0] = angle
    robot.set_joints(joints)

    transistor.laserON()
    print(laser.measure())
    transistor.laserOff()

print(robot.get_joints())
print(robot.get_external_axis())


# robot.set_joints([0, -135, 55, 0, 105, 4])

circle_radius = 60
z_stepsize = 10
max_depth = -70
azimuthPoints = 8
offset = -50

points = generate_Scan_points_Cylinder.generate_scan_points_cylinder(
    circle_radius, z_stepsize, max_depth, azimuthPoints, offset
)
"""
robot.set_cartesian(
    [
        [0, 0, -50],
        [0.0, -0.707, -0.0, 0.707],
    ]
)
"""
print("Robot Coordinate: ", robot_Control.fetch_Robot_Coordinates(robot))


"""laser.laserOn()
    if isinstance(laser.measure(), float):
        laser_data.append(laser.measure())
    laser.laserOff()
print(laser_data)
"""
# robot_Control.reset_Robot_Pos(robot)

# robot_Control.return_Robot_To_Start(robot)

robot_Control.close_Connection(robot)
