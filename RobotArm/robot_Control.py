#!/bin/python3

from RobotArm import abb


def connect_to_robot():
    "Attempts to create TCP connection to robot"
    return abb.Robot()


def fetch_robot_coordinates(robot):
    return robot.get_cartesian()


def set_reference_coordinate_system(robot, reference_coordinate):
    "Changes the reference coordinate system of the robot, offset in relation to the robots origin(base)"
    robot.set_workobject([reference_coordinate, [0.99984, 0.01793, 0.00143, 0.00229]])
    # 0.11, 64, 694.98
    # 0.71689, 0.00791, 0.69706, 0.01025


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


def return_robot_to_start(robot):
    robot.set_joints([0, -135, 55, 0, 105, 0, 0])


def close_connection(robot):
    "Returns robot to start and closes the TCP connection to robot"
    return_robot_to_start(robot)
    robot.close()


def robot_init(tool):
    """Sets initial parameters of the robot

    1 for laser TCP

    2 for Antenna TCP
    """
    robot = connect_to_robot()
    set_reference_coordinate_system(robot, [0, 0, 758.01])
    set_robot_tool(robot, tool)
    set_robot_speed(robot, [75, 25, 50, 25])
    return_robot_to_start(robot)

    return robot
