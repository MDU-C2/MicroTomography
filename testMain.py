from time import sleep
import os.path
import pandas as pd
import numpy as np


from RobotArm import robot_Control, generate_Scan_points_Cylinder
from Laser import optoNCDT1402
from RaspberryPi import transistor

circle_radius = 120
z_stepsize = 10
max_depth = -60
azimuthPoints = 16
offset = -40
elevationPoints = 10
zMin = -60

pointsCylinder = generate_Scan_points_Cylinder.generate_scan_points_cylinder(
    circle_radius, z_stepsize, max_depth, azimuthPoints, offset
)

points = pointsCylinder[0:11]
pointLast = pointsCylinder[-11:]

points += pointLast


pointsSphere = generate_Scan_points_Cylinder.generate_scan_points_halfSphere(
    circle_radius, azimuthPoints, elevationPoints, zMin, offset
)
print(pointsCylinder)
laser = optoNCDT1402.optoNCDT1402("/dev/ttyUSB0")  # Serial port of the Raspberry
transistor.init()

robot = robot_Control.connect_To_Robot()

robot_Control.set_Reference_Coordinate_System(robot, [0.03, -7.47, 760.67])

robot_Control.set_Robot_Tool(robot, 1)

robotSpeed = [75, 25, 50, 25]

filenameArray = ["file" + str(x) + ".csv" for x in range(1)]
rawfilenameArray = ["rawfile" + str(x) + ".csv" for x in range(10)]

for filename, rawfilename in zip(filenameArray, rawfilenameArray):
    laser_data = []
    raw_laser_data = []
    visitedOrigin = False
    robot_Control.set_Robot_Speed(robot, robotSpeed)

    # robot_Control.return_Robot_To_Start(robot)

    for point in pointsCylinder:
        alteredPoint = [point[0], [1, 0, 0, 0]]
        if round(point[0][0], 4) != 0 or round(point[0][1], 4) != 0:
            print(point)
            robot_Control.move_Robot_Linear(robot, point)
            sleep(2)
            print("Robot Coordinate: ", robot_Control.fetch_Robot_Coordinates(robot))

        elif not visitedOrigin:
            print(point)
            robot_Control.move_Robot_Linear(robot, point)
            sleep(1)
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
    print(
        "difference Z :",
        rawdata.max(axis=0)["Laser Distance"] - rawdata.min(axis=0)["Laser Distance"],
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

    # robot_Control.return_Robot_To_Start(robot)


robot_Control.close_Connection(robot)
