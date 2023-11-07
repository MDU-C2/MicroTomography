# Main code to control the system. Enables the user to choose the desired scan pattern and paramters for it.
# Produces a csv file with the point cloud of the laser data.

import sys
import os

pathname = os.getcwd()

sys.path.append("../Microtomography")

from RobotArm.scan_breast_phantom import scan_points

from ObjectReconstruction.read_save_csv import read_csv
from ObjectReconstruction.read_save_csv import save_csv


# Control if the user input is valid.
def get_integer_input(prompt, negative):
    while True:
        user_input = input(prompt)
        if user_input.replace(".", "", 1).lstrip("-").isdigit():
            value = int(user_input)  # We want integers
            if value < 0 and negative:  # The value is negative
                return value
            elif value >= 0 and not negative:  # The value is zero or positive
                return value
        print("Please enter a valid number.")


def cylinder():
    print("Please enter the following desired parameters:")
    radius = get_integer_input("Radius of the cylinder: ", negative=False)
    z_stepsize = get_integer_input(
        "Number of mm between each z-plane: ", negative=False
    )
    z_min = get_integer_input("Lowest point of the cylinder: ", negative=True)
    azimuth_points = get_integer_input(
        "Number of points in the azimuth angle:", negative=False
    )
    z_offset = get_integer_input("Offset in the z-axis:", negative=True)
    laser_angle = get_integer_input(
        "The angle of the end effector to point the laser upwards by:", negative=False
    )

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
    radius = get_integer_input("Radius of the half-sphere: ", negative=False)
    azimuth_points = get_integer_input(
        "Number of points in the azimuth plane: ", negative=False
    )
    elevation_points = get_integer_input(
        "Number of points in the elevation plane: ", negative=False
    )
    z_min = get_integer_input(
        "How low the half-sphere should go in the z-axis: ", negative=True
    )
    z_offset = get_integer_input("Offset in the z-axis:", negative=True)

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
    data_values = read_csv(file_name)
    save_csv(file_name, data_values)

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
