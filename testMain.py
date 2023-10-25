from time import sleep
import os.path
import pandas as pd
import numpy as np

from RobotArm import robot_Control, generate_Scan_points_Cylinder
from Laser import optoNCDT1402
from RaspberryPi import transistor

circle_radius = 120
z_stepsize = 10
max_depth = -55
azimuthPoints = 8
offset = -25
elevationPoints = 5
zMin = -90

pointsCylinder = generate_Scan_points_Cylinder.generate_scan_points_cylinder(
    circle_radius, z_stepsize, max_depth, azimuthPoints, offset
)

pointsSphere = generate_Scan_points_Cylinder.generate_scan_points_halfSphere(
    circle_radius, azimuthPoints, elevationPoints, zMin, offset
)

laser = optoNCDT1402.optoNCDT1402("/dev/ttyUSB0")  # Serial port of the Raspberry
transistor.init()

robot = robot_Control.connect_To_Robot()

robot_Control.set_Reference_Coordinate_System(robot, [0, 0, 758.01])

robot_Control.set_Robot_Tool(robot, 1)

robotSpeed = [75, 25, 50, 25]

filenameArray = ["file" + str(x) + ".csv" for x in range(10)]
rawfilenameArray = ["rawfile" + str(x) + ".csv" for x in range(10)]

for filename, rawfilename in zip(filenameArray, rawfilenameArray):
    laser_data = []
    raw_laser_data = []
    visitedOrigin = False
    robot_Control.set_Robot_Speed(robot, robotSpeed)

    robot_Control.return_Robot_To_Start(robot)

    for point in pointsCylinder:
        if round(point[0][0], 4) != 0 or round(point[0][1], 4):
            print(point)
            robot_Control.move_Robot_Linear(robot, point)
            sleep(0.5)
            print("Robot Coordinate: ", robot_Control.fetch_Robot_Coordinates(robot))

        elif not visitedOrigin:
            print(point)
            robot_Control.move_Robot_Linear(robot, point)
            sleep(0.5)
            print("Robot Coordinate: ", robot_Control.fetch_Robot_Coordinates(robot))
            visitedOrigin = True
        else:
            print("Skipping origin...")

        transistor.laserON()

        laser_point = laser.measure()
        if isinstance(laser_point, float):
            laser_data.append(
                generate_Scan_points_Cylinder.transform_laser_distance(
                    point, laser_point
                )
            )
            raw_laser_data.append(np.append(point[0], laser_point))
        transistor.laserOff()

        # laser.laserOff()
        print("Laser measurement: " + str(laser_point))

    print(laser_data)

    data = pd.DataFrame(laser_data, columns=["X_value", "Y_value", "Z_value"])
    rawdata = pd.DataFrame(
        raw_laser_data, columns=["X_value", "Y_value", "Z_value", "Laser Distance"]
    )
    file_path = os.path.join("testData", filename)
    file_path_raw = os.path.join("testData", rawfilename)
    # file_path = filedialog.asksaveasfilename(
    #    defaultextension=".csv", filetypes=[("CSV Files", "*.csv")]
    # )

    # if file_path:
    with open(file_path, "w", newline="") as csvfile:
        # Save the DataFrame to a CSV file

        data.to_csv(
            csvfile, index=False
        )  # Specify index=False to avoid writing row numbers as a column

    with open(file_path_raw, "w", newline="") as csvfile:
        # Save the DataFrame to a CSV file

        rawdata.to_csv(
            csvfile, index=False
        )  # Specify index=False to avoid writing row numbers as a column

    robot_Control.return_Robot_To_Start(robot)


robot_Control.close_Connection(robot)
