#!/bin/python3

from RobotArm import abb

def connect_To_Robot():
    "Attempts to create TCP connection to robot"
    return abb.Robot()


def fetch_Robot_Coordinates(robot):
    return robot.get_cartesian()


def set_Reference_Coordinate_System(robot, reference_Coordinate):
    "Changes the reference coordinate system of the robot, offset in relation to the robots origin(base)"
    robot.set_workobject([reference_Coordinate, [1, 0, 0, 0]])
    # 0.11, 64, 694.98


def move_Robot_Linear(robot, coordinates):
    "Moves the robot in a linear motion to the given coordinates"
    robot.set_cartesian(coordinates)


def set_Robot_Speed(robot, speed):
    """Set the speed of the robot

    speed: [robot TCP linear speed (mm/s), TCP orientation speed (deg/s),
                external axis linear, external axis orientation]"""
    robot.set_speed(speed)


# Under construction
def set_Calibration(robot):
    "Set the current calibration TCP to new workframe"
    input(
        "Press enter when arm is in calibration position to set new calibration point..."
    )
    robot.set_calibration()


def set_Robot_Tool(robot, tool):
    """Change the tool TCP of the robot.

    1 for LASER TCP

    2 for Antenna TCP
    """
    robot.change_current_tool(tool)


def return_Robot_To_Start(robot):
    # robot.set_joints([0, -100, 0, 0, 105, 45])
    # robot.set_joints([0, -135, 55, 0, 105, 45])
    # robot.set_cartesian([[-86.04, 16.4, -292.5], [0.54, 0.001, 0.842, 0.001]])
    robot.set_joints([0, -135, 55, 0, 105, 45])
    robot.set_external_axis(0)


def close_Connection(robot):
    "Close TCP connection to robot"
    robot.close()
    print("Program closed...")
