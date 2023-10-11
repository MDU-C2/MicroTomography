#!/bin/python3

import abb


def connect_To_Robot():
    "Attempts to create TCP connection to robot"
    return abb.Robot()


def set_Reference_Coordinate_System(robot):
    "Changes the reference coordinate system of the robot, offset in relation to the robots origin(base)"
    robot.set_workobject([[4.76, -62.64, 696.66], [1, 0, 0, 0]])


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


def close_Connection(robot):
    "Close TCP connection to robot"
    robot.close()
    print("Program closed...")
