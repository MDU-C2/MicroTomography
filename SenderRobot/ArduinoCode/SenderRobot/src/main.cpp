#include <Arduino.h>
#include <Stepper.h>

// Arduino PWM Speed Control：
int E1 = 5;
int M1 = 4;
int E2 = 6;
int M2 = 7;

const int stepsPerRevolution = 400;

// Initialize the stepper library on pins 8 through 11:
Stepper myStepper = Stepper(stepsPerRevolution, 4, 5, 6, 7);

void setup()
{
  // Set the motor speed (RPMs):
  myStepper.setSpeed(100);
}

void loop()
{
  // Step one revolution in one direction:
  myStepper.step(200);

  delay(2000);

  // Step on revolution in the other direction:
  myStepper.step(-200);

  delay(2000);
}
