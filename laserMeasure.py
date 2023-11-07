from RobotArm import robot_Control, generate_Scan_points_Cylinder
from Laser import optoNCDT1402
from RaspberryPi import transistor
from time import sleep


laser = optoNCDT1402.optoNCDT1402("/dev/ttyUSB0")  # Serial port of the Raspberry
transistor.init()
transistor.laserOff()


transistor.laserON()
print(laser.measure())
transistor.laserOff()
