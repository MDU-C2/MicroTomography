# Main code to control the system. Enables the user to choose the desired scan pattern and paramters for it.
# Preforms the laser scan and produces a csv file with the point cloud of the laser data.

import sys
import os

pathname = os.getcwd()

sys.path.append("../Microtomography")

from RobotArm.scan_breast_phantom import scan_points
from ObjectReconstruction.read_save_csv import save_csv


# Control if the user input is valid.
def get_numeric_input(prompt, negative, allow_float):
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


def save_laser_scan(file_name, data):
    # Save the data in a CSV file.
    save_csv(file_name, data)

    print("The generated point cloud has been saved in a file.")


# ------------ Main starts here ---------------------

print("Hello, please pick a pattern for the scanning")
choice = input("Enter 1 for cylindrical pattern and 2 for half-sphere pattern: ")

while choice not in ("1", "2"):
    print("Try again.")
    choice = input("Enter 1 or 2: ")

if choice == "1":
    result = cylinder()
    print(result)
elif choice == "2":
    result = half_sphere()
    print(result)


file_name = input(
    "Please enter your desired name for the file where the data will be saved:"
)
save_laser_scan(file_name + ".csv", result)

# -----------------------------------------------------
