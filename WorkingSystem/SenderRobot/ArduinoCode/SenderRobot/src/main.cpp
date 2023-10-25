#include <Arduino.h>

#include <AccelStepper.h>

// Arduino PWM Speed Control：
int M1 = 4;
int E1 = 5;

int E2 = 6;
int M2 = 7;

void setup()
{
  /*pinMode(M1, OUTPUT);
  pinMode(M2, OUTPUT);

  Serial.begin(115200);*/
}

void loop()
{

    AccelStepper stepper1(1, 2, 5); // (Type of driver: with 2 pins, STEP, DIR)

    /*int time = 600;
    int power = 100;

    // Steg 1
    analogWrite(E1, 0);
    digitalWrite(M1, LOW);

    analogWrite(E2, power);
    digitalWrite(M2, LOW);

    delayMicroseconds(time);

    // Steg 2
    analogWrite(E1, power);
    digitalWrite(M1, HIGH);

    analogWrite(E2, power);
    digitalWrite(M2, LOW);

    delayMicroseconds(time);

    // Steg 3
    analogWrite(E1, power);
    digitalWrite(M1, HIGH);

    analogWrite(E2, 0);
    digitalWrite(M2, LOW);

    delayMicroseconds(time);

    // Steg 4
    analogWrite(E1, power);
    digitalWrite(M1, HIGH);

    analogWrite(E2, power);
    digitalWrite(M2, HIGH);

    delayMicroseconds(time);

    // Steg 5
    analogWrite(E1, 0);
    digitalWrite(M1, LOW);

    analogWrite(E2, power);
    digitalWrite(M2, HIGH);

    delayMicroseconds(time);

    // Steg 6
    analogWrite(E1, power);
    digitalWrite(M1, LOW);

    analogWrite(E2, power);
    digitalWrite(M2, HIGH);

    delayMicroseconds(time);

    // Steg 7
    analogWrite(E1, power);
    digitalWrite(M1, LOW);

    analogWrite(E2, 0);
    digitalWrite(M2, LOW);

    delayMicroseconds(time);

    // Steg 8
    analogWrite(E1, power);
    digitalWrite(M1, LOW);

    analogWrite(E2, power);
    digitalWrite(M2, LOW);

    delayMicroseconds(time);*/
  

  /*
  //Steg 1
  analogWrite(E1, 80);
  digitalWrite(M1, LOW);

  analogWrite(E2, 80);
  digitalWrite(M2, LOW);

  delay(5);

  //Steg 2
  analogWrite(E1, 80);
  digitalWrite(M1, LOW);

  analogWrite(E2, 80);
  digitalWrite(M2, HIGH);

  delay(5);

  //Steg 3
  analogWrite(E1, 80);
  digitalWrite(M1, HIGH);

  analogWrite(E2, 80);
  digitalWrite(M2, HIGH);

  delay(5);

  //Steg 4
  analogWrite(E1, 80);
  digitalWrite(M1, HIGH);

  analogWrite(E2, 80);
  digitalWrite(M2, LOW);

  delay(5);
  */
}