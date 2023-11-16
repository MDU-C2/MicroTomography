import sys
import os

pathname = os.getcwd()

sys.path.append("../Microtomography")


import RPi.GPIO as GPIO

transistorPin = 22 # Pin of the Raspberry Pi which the transistor is connected to


def laserOff():
    GPIO.output(transistorPin, GPIO.LOW)


def laserON():
    GPIO.output(transistorPin, GPIO.HIGH)


def init():
    "Initialize the GPIO pin used by the transistor and turn off the laser"
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(transistorPin, GPIO.OUT)
    laserOff()
