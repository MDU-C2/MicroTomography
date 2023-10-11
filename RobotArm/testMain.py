import robot_Control
import generate_Scan_points_Cylinder


circle_diameter = 120
z_stepsize = 10
max_depth = -50
azimuthPoints = 16

points = generate_Scan_points_Cylinder.generate_scan_points_cylinder(
    circle_diameter, z_stepsize, max_depth, azimuthPoints
)

robot = robot_Control.connect_To_Robot()

robot_Control.set_Reference_Coordinate_System(robot)

robot.set_calibration()

robot_Control.set_Robot_Tool(robot, 1)

robotSpeed = [75, 25, 50, 25]

robot_Control.set_Robot_Speed(robot, robotSpeed)
# robot_Control.reset_Robot_Pos(robot)

for point in points:
    robot_Control.move_Robot_Linear(robot, point)

# robot_Control.reset_Robot_Pos(robot)

robot_Control.close_Connection(robot)
