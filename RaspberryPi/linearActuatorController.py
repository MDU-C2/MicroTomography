import RPi.GPIO as GPIO
import time

# Define GPIO pins for TB6600 control
PUL_PIN = 17  # GPIO 17 for pulse
DIR_PIN = 27  # GPIO 27 for direction
# ena_pin = 22  # GPIO 22 for enable
# total_steps_changes = 0 # Global value_ calculate the steps +1 for step up and -1 for step down


class linear_actuator:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PUL_PIN, GPIO.OUT)
        GPIO.setup(DIR_PIN, GPIO.OUT)
        self.total_steps_changes = 0

    # Function to calculate the number of steps needed to move a certain linear distance
    def calculate_steps(self, desired_distance, step_size=0.01):
        return int(desired_distance / step_size)

    # function to move the motor when gien the steps
    def move(self, steps_to_move):
        delay = 0.001

        for _ in range(steps_to_move):
            GPIO.output(PUL_PIN, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(PUL_PIN, GPIO.LOW)
            time.sleep(delay)
            if (
                GPIO.input(DIR_PIN) == GPIO.HIGH
            ):  # Depending on direction of the steps, it counts the amount of steps
                self.total_steps_changes += 1
            elif self.total_steps_changes > 10000:
                break

        # return total_steps_changes

    def move_to_desired_location_upwards(
        self,desired_distance_mm
    ):  # Get distance from app.py
        GPIO.output(DIR_PIN, GPIO.HIGH)  # set the direction UP

        #desired_distance_mm = float(input("Enter the desired distance (mm)")) # choosing the desired distance in mm

        steps_to_move = self.calculate_steps(
            desired_distance_mm
        )  # calculating the desired distance in steps

        self.move(steps_to_move)  # call the move function

        #GPIO.cleanup()
        # return total_steps_changes

    def move_to_zeroLocation(self):  # This function move the motor to zero location
        GPIO.output(DIR_PIN, GPIO.LOW)

        delay = 0.001

        for _ in range(self.total_steps_changes):
            GPIO.output(PUL_PIN, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(PUL_PIN, GPIO.LOW)
            time.sleep(delay)

        # GPIO.cleanup()

    def move_up_1mm(self):
        GPIO.output(DIR_PIN, GPIO.HIGH)
        delay = 0.001
        t = 100
        for _ in range(t):
            GPIO.output(PUL_PIN, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(PUL_PIN, GPIO.LOW)
            time.sleep(delay)

        # GPIO.cleanup()

    def move_down_1mm(self):
        GPIO.output(DIR_PIN, GPIO.LOW)
        delay = 0.001
        t = 100

        for _ in range(t):
            GPIO.output(PUL_PIN, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(PUL_PIN, GPIO.LOW)
            time.sleep(delay)

        # GPIO.cleanup()

    def move_actuator(self):
        while True:
            # print(total_steps_changes)
            # print("\n")

            ##For control the values between 0 < x < 10000
            if self.total_steps_changes < 0:
                self.total_steps_changes = 0
            elif self.total_steps_changes > 10000:
                self.total_steps_changes = 10000

            choice = input(
                "Enter: 1:(desired location), 2:(move to zero), 3:(up 1mm), 4:(down 1mm):, q:(quit)"
            )

            if choice == "1":

                self.move_to_desired_location_upwards()

            elif choice == "2":
                self.move_to_zeroLocation()
                self.total_steps_changes = 0

            elif choice == "3":
                self.move_up_1mm()
                self.total_steps_changes += 100

                # for every move_up function the total_steps_changes are added with 100 steps = 1mm
            elif choice == "4":
                self.move_down_1mm()
                self.total_steps_changes -= 100

            elif choice == "q":
                GPIO.cleanup()
                break

            else:
                print("Invalid input")
            # char =getch.getch()

    ## example for how the master script would look líke
    # it should be within a loop so that the total steps


if __name__ == "__main__":
    lin = linear_actuator()
    lin.move_actuator()
