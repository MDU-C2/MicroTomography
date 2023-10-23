import RPi.GPIO as GPIO

transistorPin = 22


def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(transistorPin, GPIO.OUT)


def laserOff():
    GPIO.output(transistorPin, GPIO.LOW)


def laserON():
    GPIO.output(transistorPin, GPIO.HIGH)
