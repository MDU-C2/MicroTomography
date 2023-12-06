import RPi.GPIO as GPIO
import time

# Define GPIO pins for TB6600 control
PUL_PIN = 17  # GPIO 17 for pulse
DIR_PIN = 27  # GPIO 27 for direction
# ena_pin = 22  # GPIO 22 for enable

class linear_actuator:
    def __init__(self):
        #Set up
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PUL_PIN, GPIO.OUT)
        GPIO.setup(DIR_PIN, GPIO.OUT)

    # function to move the motor when gien the steps
    def move(self, steps_to_move):
        delay = 0.001

        for _ in range(steps_to_move):
            GPIO.output(PUL_PIN, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(PUL_PIN, GPIO.LOW)
            time.sleep(delay)

            if steps_to_move > 10000 or steps_to_move < 0:
                break
            elif (GPIO.input(DIR_PIN) == GPIO.HIGH):  # Depending on direction of the steps, it counts the amount of steps
                steps_to_move += 1
            elif(GPIO.input(DIR_PIN) == GPIO.LOW):
                steps_to_move -= 1

    def move_to_desired_location(self, currentdistance, desired_distance_mm, direction):  # Get distance from app.py
        if direction == 1:
            GPIO.output(DIR_PIN, GPIO.HIGH)  # set the direction UP
        elif direction == 2:
            GPIO.output(DIR_PIN, GPIO.LOW)  # set the direction Down

        steps_to_move = int(abs(currentdistance - desired_distance_mm) * 100)  # calculating the desired distance in steps

        # For control the values between 0 < x < 10000
        if steps_to_move <= 0:
            steps_to_move = 0
        elif steps_to_move > 10000:
            steps_to_move = 10000

        self.move(steps_to_move)  # call the move function

    def move_up_1mm(self, steps):
        GPIO.output(DIR_PIN, GPIO.HIGH)
        delay = 0.001
        t = 100 #100 times ON and OFF = 1mm movement

        steps = steps + 1

        if steps > 100:
            steps = 100

        for _ in range(t):
            GPIO.output(PUL_PIN, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(PUL_PIN, GPIO.LOW)
            time.sleep(delay)
        
        return steps

    def move_down_1mm(self, steps):
        GPIO.output(DIR_PIN, GPIO.LOW)
        delay = 0.001
        t = 100 #100 times ON and OFF = 1mm movement

        steps = steps - 1

        if steps < 0:
            steps = 0

        for _ in range(t):
            GPIO.output(PUL_PIN, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(PUL_PIN, GPIO.LOW)
            time.sleep(delay)

        return steps
