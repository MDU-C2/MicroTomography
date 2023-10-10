#!/bin/python3

import abb


def connect_To_Robot():
    "Attempts to create TCP connection to robot"
    return abb.Robot()


def set_Reference_Coordinate_System(robot):
    "Changes the reference coordinate system of the robot, offset in relation to the robots origin(base)"
    robot.set_workobject([[0, 0, 755], [1, 0, 0, 0]])


def move_Robot_Linear(robot, coordinates):
    "Moves the robot in a linear motion to the given coordinates"
    robot.set_cartesian(coordinates)


def set_Robot_Speed(robot, speed):
    """Set the speed of the robot

    speed: [robot TCP linear speed (mm/s), TCP orientation speed (deg/s),
                external axis linear, external axis orientation]"""
    robot.set_speed(speed)


def set_Calibration(robot):
    "Set the current calibration TCP to new workframe"
    robot.set_calibration()


def close_Connection(robot):
    "Close TCP connection to robot"
    robot.close()
    print("Program closed...")
