from optoNCDT1402 import optoNCDT1402
from time import sleep

# Change the comPort to the connected port on the computer
laser = optoNCDT1402(comPort="/dev/ttyUSB0")

for _ in range(1000):
    sleep(3)
    print(f"Laser On: {laser.laserOn()}")
    a = laser.measure()
    print(a)
    print(f"Laser Off: {laser.laserOff()}\n")
