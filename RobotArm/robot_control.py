#!/bin/python3

from RobotArm import abb


def connect_to_robot():
    "Attempts to create TCP connection to robot"
    return abb.Robot()


def fetch_robot_coordinates(robot):
    return robot.get_cartesian()


def set_reference_coordinate_system(robot, reference_coordinate):
    """Changes the reference coordinate system of the robot, offset in relation to the robots origin(base)

    Expected input for "reference_coordinate": [[x, y, z], [q1, q2, q3, q4]]
    """
    robot.set_workobject(reference_coordinate)


def move_robot_linear(robot, coordinates):
    "Moves the robot in a linear motion to the given coordinates"
    robot.set_cartesian(coordinates)


def set_robot_speed(robot, speed):
    """Set the speed of the robot

    speed: [robot TCP linear speed (mm/s), TCP orientation speed (deg/s),
                external axis linear, external axis orientation]"""
    robot.set_speed(speed)


# Under construction
def set_calibration(robot):
    "Set the current calibration TCP to new workframe"
    input(
        "Press enter when arm is in calibration position to set new calibration point..."
    )
    robot.set_calibration()


def set_robot_tool(robot, tool):
    """Change the tool TCP of the robot.

    1 for LASER TCP

    2 for Antenna TCP
    """
    robot.change_current_tool(tool)


def set_zone_use(robot, zone_use):
    """Set use of zone traversment.

    False: for no zone traversement

    True: for zone traversement
    """
    if zone_use == True:
        robot.use_zone_traverse(1)
    else:
        robot.use_zone_traverse(0)


def return_robot_to_start(robot):
    robot.set_joints([0, -135, 55, 0, 105, 0, 0])


def close_connection(robot):
    "Returns robot to start and closes the TCP connection to robot"
    return_robot_to_start(robot)
    robot.close()


def robot_init(tool):
    """Connects to and sets initial parameters of the robot

    tool == 1: for laser TCP

    tool == 2: for Antenna TCP
    """
    robot = connect_to_robot()
    set_reference_coordinate_system(
        robot,
        [
            [-3.40, -6.31, 760.2787866568916],
            [0.9999534, 0.0094194, 0.0014893, 0.0015269],
        ],
    )

    """
    [0.9999534, 0.0094194, 0.0014893, 0.0015269]
    [0.9999509211136645,0.009829618166903913,0.0012385159580043847,6.989160936131759e-06]
    [9.99954527e-01, 9.41712207e-03, 1.50357889e-03, 9.45543129e-06]
    760.3715408113393
    [0.20, -5.41, 759.24] where fetched using the calibration TCP, when aimed at nipple it seems to be aiming slightly left
    When arm is in last quadrant it almost perfectly center.

    [0.6, -7.5, 759.24] where fetched by pointing laser from under the breast phantom and manually moving the arm until laser was centered
    Laser was sligthly left during first half but became more centered after second half. Some points missed the breast phantom during the first
    half which did not occur during the previous coordinates

    """
    set_robot_tool(robot, tool)
    set_robot_speed(robot, [75, 25, 50, 25])
    return_robot_to_start(robot)

    return robot
