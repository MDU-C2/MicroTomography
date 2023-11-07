from time import sleep
import os.path
import pandas as pd
import numpy as np


from RobotArm import robot_Control, generate_Scan_points_Cylinder
from Laser import optoNCDT1402
from RaspberryPi import transistor


laser = optoNCDT1402.optoNCDT1402("/dev/ttyUSB0")  # Serial port of the Raspberry
transistor.init()

robot = robot_Control.connect_To_Robot()

robot_Control.set_Reference_Coordinate_System(robot, [0, 0, 0])

robot_Control.set_Robot_Tool(robot, 1)

robotSpeed = [75, 25, 50, 25]

calibrationPoints = [
    [215, -9, 700],
    [336, 94, 700],
    [340, 215, 700],
    [124, 89, 700],
    [45, 230, 700],
    [-128, 103, 700],
    [-270, 225, 700],
    [-400, 142, 700],
    [-222, 22, 700],
    [-420, 165, 700],
    [-230, -220, 700],
    [-105, 80, 700],
    [-25, -220, 700],
    [110, -63, 700],
    [290, -178, 700],
    [200, -13, 700],
]

rawfilenameArray = ["calibrationTest" + str(x) + ".csv" for x in range(10)]

for filename, rawfilename in zip(rawfilenameArray, rawfilenameArray):
    laser_data = []
    raw_laser_data = []
    visitedOrigin = False
    robot_Control.set_Robot_Speed(robot, robotSpeed)

    # robot_Control.return_Robot_To_Start(robot)

    for point in calibrationPoints:
        alteredPoint = [point, [1, 0, 0, 0]]
        if round(point[0], 4) != 0 or round(point[1], 4) != 0:
            print(point)
            robot_Control.move_Robot_Linear(robot, alteredPoint)
            sleep(3)
            print("Robot Coordinate: ", robot_Control.fetch_Robot_Coordinates(robot))

        elif not visitedOrigin:
            print(point)
            robot_Control.move_Robot_Linear(robot, alteredPoint)
            sleep(3)
            print("Robot Coordinate: ", robot_Control.fetch_Robot_Coordinates(robot))
            visitedOrigin = True
        else:
            print("Skipping origin...")

        transistor.laserON()

        laser_point = laser.measure()
        if isinstance(laser_point, float):
            raw_laser_data.append(np.append(point, laser_point))
        transistor.laserOff()

        # laser.laserOff()
        print("Laser measurement: " + str(laser_point))

    print(laser_data)

    rawdata = pd.DataFrame(
        raw_laser_data, columns=["X_value", "Y_value", "Z_value", "Laser Distance"]
    )
    print(
        "difference Z :",
        rawdata.max(axis=0)["Laser Distance"] - rawdata.min(axis=0)["Laser Distance"],
    )
    file_path_raw = os.path.join("testData", rawfilename)
    # file_path = filedialog.asksaveasfilename(
    #    defaultextension=".csv", filetypes=[("CSV Files", "*.csv")]
    # )

    with open(file_path_raw, "w", newline="") as csvfile:
        # Save the DataFrame to a CSV file

        rawdata.to_csv(
            csvfile, index=False
        )  # Specify index=False to avoid writing row numbers as a column

    # robot_Control.return_Robot_To_Start(robot)


robot_Control.close_Connection(robot)
