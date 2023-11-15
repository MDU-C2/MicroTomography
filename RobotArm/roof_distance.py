import sys
import os

pathname = os.getcwd()

sys.path.append(r"/home/mwi/Repositories/MicroTomography")

from RobotArm import robot_control
from time import sleep
from Laser.optoNCDT1402 import optoNCDT1402
from RaspberryPi import transistor

laser = optoNCDT1402(noMeasurements=15)

transistor.init()
robot = robot_control.robot_init(1)
laser.setMovingAverage(1)
z = -130

# robot_control.return_robot_to_start(robot)
robot_control.move_robot_linear(robot, [[0, 0, z], [1, 0, 0, 0]])
sleep(4)
i = 0
z_data = []
while True:
    transistor.laserON()
    data = laser.measure()
    transistor.laserOff()
    print(data)

    if isinstance(data, float):
        diff = z + data
        true_z = 760.2787866568916 + diff
        print(f"diff: {diff}, true_z: {true_z}")
        z_data.append(true_z)
        i += 1
        if i == 20:
            break

    sleep(1)

print(sum(z_data) / len(z_data))
