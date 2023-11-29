# Main code to control the system. Enables the user to choose the desired scan pattern and paramters for it.
# Preforms the laser scan and produces a csv file with the point cloud of the laser data.

import sys
import os

pathname = os.getcwd()

sys.path.append("../Microtomography")

from RobotArm.scan_breast_phantom import scan_points, find_nipple, find_lowest_point
from ObjectReconstruction.read_save_csv import save_csv

from ObjectReconstruction.surface_reconstruction import (
    poisson_surface_reconstruction,
)

from zvb.titi_bakonkadonk_brest_8008 import mw_boob
from RaspberryPi.linearActuatorController import linear_actuator


# Control if the user input is valid.
def get_numeric_input(
    prompt: str, negative: (True | False | None), allow_float: bool
) -> int | float:
    """Prompts the user with a string and checks whether the user inputs the correct type of number based on the parameters.

    Parameters
    ----------
    prompt : str
        The prompth for the user to answer.
    negative : True  |  False  |  None
        Parameter to decide if the value should be negative, positive or if it does not matter.
        True means the value must be negative.
        False means it must be positive or zero.
        None means the value can be either positive or negative.
    allow_float : bool
        Parameter to decide if the value can be a float or must be int. True means it can be a float and False means it must be an integer.

    Returns
    -------
    int | float
        Returns the value based on the input parameters.
    """
    while True:
        user_input = input(prompt)
        try:
            # Check if float is allowed
            if allow_float:
                value = float(user_input)  # Allow both integer and float input
            else:
                value = int(user_input)  # Enforce integer input

            # Check if both, negative or positive is allowed
            if (
                negative is None
                or (value < 0 and negative)
                or (value >= 0 and not negative)
            ):
                return value
            else:
                print("Please enter a valid number.")
        except ValueError:
            print("Please enter a valid number.")


def get_laser_angle_input():
    while True:
        laser_angle = get_numeric_input(
            "Enter the angle of the end effector to point the laser (positive or negative):",
            negative=None,
            allow_float=True,
        )

        if -90 <= laser_angle <= 90:
            return laser_angle
        else:
            print("Invalid angle. Please enter an angle between -90 and 90 degrees.")


def cylinder():
    print("Please enter the following desired parameters:")
    radius = get_numeric_input(
        "Radius of the cylinder: ", negative=False, allow_float=True
    )
    z_stepsize = get_numeric_input(
        "Number of mm between each z-plane: ", negative=False, allow_float=False
    )
    z_min = get_numeric_input(
        "Lowest point of the cylinder: ", negative=True, allow_float=False
    )
    azimuth_points = get_numeric_input(
        "Number of points in the azimuth angle:", negative=False, allow_float=False
    )
    z_offset = get_numeric_input(
        "Offset in the z-axis:", negative=True, allow_float=True
    )

    laser_angle = get_laser_angle_input()

    scan_choice = input("To start the laser scan, please enter 1:")

    while scan_choice != "1":
        print("Try again:")
        scan_choice = input()

    # The resulting laser data.
    result = scan_points(
        radius, z_stepsize, z_min, azimuth_points, z_offset, laser_angle
    )

    print("The scan is finished.")

    return result


def half_sphere():
    print("Please enter the following desired parameters:")
    radius = get_numeric_input(
        "Radius of the half-sphere: ", negative=False, allow_float=True
    )
    azimuth_points = get_numeric_input(
        "Number of points in the azimuth plane: ", negative=False, allow_float=False
    )
    elevation_points = get_numeric_input(
        "Number of points in the elevation plane: ", negative=False, allow_float=False
    )
    z_min = get_numeric_input(
        "How low the half-sphere should go in the z-axis: ",
        negative=True,
        allow_float=True,
    )
    z_offset = get_numeric_input(
        "Offset in the z-axis:", negative=True, allow_float=True
    )

    scan_choice = input("To start the laser scan, please enter 1:")

    while scan_choice != "1":
        print("Try again:")
        scan_choice = input()

    # The resulting laser data.
    result = scan_points(radius, azimuth_points, elevation_points, z_min, z_offset)

    print("The scan is finished.")
    return result


def scan_the_nipple():
    print("Please enter the following desired parameters:")
    z_offset = get_numeric_input("z_offset: ", negative=True, allow_float=True)
    distance = get_numeric_input(
        "Distance between each point: ", negative=False, allow_float=True
    )
    side_len = get_numeric_input(
        "The length of each side: ", negative=False, allow_float=True
    )

    result_coord, result_dist, result = find_nipple(z_offset, distance, side_len)

    return result_coord, result_dist, result


def find_lowest_pointt():
    print("Please enter the following desired parameters:")
    z_offset = get_numeric_input("z_offset: ", negative=True, allow_float=True)
    result1 = find_lowest_point(z_offset)

    return result1


def save_laser_scan(file_name, data):
    # Save the data in a CSV file.
    save_csv(file_name, data)

    print("The generated point cloud has been saved in a file.")


def mw_scan(mesh):
    scan_type = 0
    while scan_type not in [1, 2]:
        scan_type = get_numeric_input(
            "Enter what type of scanning you want to do, 1 or circular and 2 for manual coordinates: ",
            False,
            False,
        )
    if scan_type == 1:
        radius = get_numeric_input("Enter the radius of the cylinder: ", False, True)
        z_offset = get_numeric_input("Enter the distance from the roof: ", True, True)
        azi = get_numeric_input("Enter the amount of azimouth angles: ", False, False)
        points = scan_points(radius, 0, z_offset, azi, z_offset, 0)
    if scan_type == 2:
        while True:
            number_of_points = get_numeric_input(
                "Enter the number of points you want to scan: ", False, False
            )
            if number_of_points > 0:
                break

        points = []
        for i in range(number_of_points):
            print(f"Enter coordinates for point {i}:")
            x = get_numeric_input("X coordinate: ", None, True)
            y = get_numeric_input("Y coordinate: ", None, True)
            z = get_numeric_input("Z coordinate: ", True, True)
            points.append([x, y, z])

    print("Enter distance to place the MWI antenna (mm): ")
    distance = get_numeric_input("Distance:", None, True)

    data = mw_boob(mesh, points, distance)

    return data


# ------------ Main starts here ---------------------
if __name__ == "__main__":
    print("Hello, please pick a pattern for the scanning")
    choice = input(
        "Enter 1 for cylindrical pattern and 2 for half-sphere pattern (or 3 or 4), 5 for testing MWI scann, 6 for testing the complete system from scanning to mwi scanning: "
    )

    while choice not in ("1", "2", "3", "4", "5", "6"):
        print("Try again.")
        choice = input("Enter 1, 2, 3 4: ")

    if choice == "1":
        result = cylinder()
        print(result)
    elif choice == "2":
        result = half_sphere()
        print(result)
    elif choice == "3":
        result1, result2, result = scan_the_nipple()
        print(result1, result2)
    elif choice == "4":
        result = find_lowest_pointt()
    elif choice == "6":
        result = cylinder()
        mesh = poisson_surface_reconstruction(result, save=False)
        mw_data = mw_scan(mesh)

    if choice != "5":
        file_name = input(
            "Please enter your desired name for the file where the data will be saved:"
        )
        save_laser_scan(file_name + ".csv", result)
    from ObjectReconstruction.read_save_csv import read_csv

    result = read_csv("scanned_data/2023-11-29-09_01-brest_no_nipple.csv")
    mesh = poisson_surface_reconstruction(result, save=False)

    la = linear_actuator()
    la.move_actuator()

    mw_data = mw_scan(mesh)

    # -----------------------------------------------------
