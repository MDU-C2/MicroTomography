import RPi.GPIO as GPIO
import time

# Define GPIO pins for TB6600 control
pul_pin = 17  # GPIO 17 for pulse
dir_pin = 27  # GPIO 27 for direction
#ena_pin = 22  # GPIO 22 for enable
#total_steps_changes = 0 # Global value_ calculate the steps +1 for step up and -1 for step down

GPIO.setmode(GPIO.BCM)
GPIO.setup(pul_pin, GPIO.OUT)
GPIO.setup(dir_pin, GPIO.OUT)

# Function to calculate the number of steps needed to move a certain linear distance
def calculate_steps(desired_distance, step_size=0.01):
    return int(desired_distance / step_size)

# function to move the motor when gien the steps
def move(steps_to_move, total_steps_changes): 
        
        delay= 0.001

        for _ in range(steps_to_move):
            GPIO.output(pul_pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(pul_pin, GPIO.LOW)
            time.sleep(delay)
            if GPIO.input(dir_pin) == GPIO.HIGH:# Depending on direction of the steps, it counts the amount of steps
                total_steps_changes += 1
            elif total_steps_changes > 10000:
                break

        return total_steps_changes


def move_to_desired_location_upwards(desired_distance_mm): #Get distance from app.py
     GPIO.output(dir_pin, GPIO.HIGH) # set the direction UP

     #desired_distance_mm = float(input("Enter the desired distance (mm)")) # choosing the desired distance in mm

     steps_to_move = calculate_steps(desired_distance_mm) # calculating the desired distance in steps

     total_steps_changes = move(steps_to_move,total_steps_changes) # call the move function 

     GPIO.cleanup()
     return total_steps_changes

def move_to_zeroLocation(total_steps_changes): # This function move the motor to zero location
        GPIO.output(dir_pin, GPIO.LOW) 

        delay= 0.001

        for _ in range(total_steps_changes):
            GPIO.output(pul_pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(pul_pin, GPIO.LOW)
            time.sleep(delay)

        GPIO.cleanup()

def move_up_1mm():
     GPIO.output(dir_pin, GPIO.HIGH)
     delay= 0.001
     t = 100
     for _ in range(t):
            GPIO.output(pul_pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(pul_pin, GPIO.LOW)
            time.sleep(delay)

     GPIO.cleanup()
     
    
def move_down_1mm():
     GPIO.output(dir_pin, GPIO.LOW)
     delay= 0.001
     t = 100

     for _ in range(t):
            GPIO.output(pul_pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(pul_pin, GPIO.LOW)
            time.sleep(delay)

     GPIO.cleanup()
     
"""
while True:

    
   # print(total_steps_changes)
   # print("\n")

   ##For control the values between 0 < x < 10000
    if total_steps_changes < 0:
        total_steps_changes = 0
    elif total_steps_changes > 10000:
         total_steps_changes = 10000
    
    #choice = input("Enter: 1:(desired location), 2:(move to zero), 3:(up 1mm), 4:(down 1mm):")
    

    if choice == '1':   
        total_steps_changes = move_to_desired_location_upwards(total_steps_changes)
        
        

    elif choice == '2':
        move_to_zeroLocation(total_steps_changes)
        total_steps_changes = 0

    elif choice == '3':
        move_up_1mm()
        total_steps_changes = total_steps_changes +100
        
        # for every move_up function the total_steps_changes are added with 100 steps = 1mm
    elif choice == '4':
        move_down_1mm()
        total_steps_changes = total_steps_changes -100
        
        
    #elif choice == 'q':
     #    break
    
    #else:
       #  print('Invalid input')
    #char =getch.getch()
"""

    




## example for how the master script would look líke 
# it should be within a loop so that the total steps


     


      