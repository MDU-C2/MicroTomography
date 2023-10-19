from RobotArm import robot_Control, generate_Scan_points_Cylinder
from Laser import optoNCDT1402
from time import sleep
from tkinter import filedialog

import pandas as pd


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

laser = optoNCDT1402.optoNCDT1402("COM3")
laser_data = []

robot = robot_Control.connect_To_Robot()

robot_Control.set_Reference_Coordinate_System(robot, [0.6, -3.85, 758.01])


robot_Control.set_Robot_Tool(robot, 1)

robotSpeed = [75, 25, 50, 25]

visitedOrigin = False
# robot_Control.set_Robot_Speed(robot, robotSpeed)

robot_Control.return_Robot_To_Start(robot)

for point in pointsCylinder:
    if round(point[0][0], 4) != 0 or round(point[0][1], 4):
        print(point)
        robot_Control.move_Robot_Linear(robot, point)
        sleep(1)
        print("Robot Coordinate: ", robot_Control.fetch_Robot_Coordinates(robot))

    elif not visitedOrigin:
        print(point)
        robot_Control.move_Robot_Linear(robot, point)
        sleep(1)
        print("Robot Coordinate: ", robot_Control.fetch_Robot_Coordinates(robot))
        visitedOrigin = True
    else:
        print("Skipping origin...")

    laser.laserOn()
    if isinstance(laser.measure(), float):
        laser_point = laser.measure()
    laser.laserOff()
    print("Laser measurement: " + str(laser_point))

    laser_data.append(
        generate_Scan_points_Cylinder.transform_laser_distance(point, laser_point)
    )

print(laser_data)



data = pd.DataFrame(laser_data, columns=['X_value', 'Y_value','Z_value'])

file_path = filedialog.asksaveasfilename(
    defaultextension=".csv",
    filetypes=[("CSV Files", "*.csv")]
)

if file_path:
    with open(file_path, 'w', newline='') as csvfile:

        df = pd.DataFrame(data)

        # Save the DataFrame to a CSV file

        df.to_csv(csvfile, index=False)  # Specify index=False to avoid writing row numbers as a column


robot_Control.return_Robot_To_Start(robot)

robot_Control.close_Connection(robot)
