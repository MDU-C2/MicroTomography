/****************************************************************************************************************************
  main.cpp

  This code allows the Arduino to recieve commands over UDP IP and move the sender robot accordingly.

  Author: Emanuel Bjurhager
 *****************************************************************************************************************************/

#include <string.h>
#include <stdio.h>
#include <Arduino.h>
#include "Ethernet_Generic.h"

#define SS_PIN 10

// Pins
const int microSwitchPin = 8;  // Pin for microswitch
const int PUL = 7;             // Pulse pin of stepper controller
const int DIR = 6;             // Direction pin of stepper controller
const int ENA = 5;             // Enable Pin (Motor on/off) of stepper controller


// For sender robot
const unsigned long stepmm = 3200; // Number of steps to move 1mm
const int max_height = 195;
double height;

// For ethernet
unsigned int localPort = 1001;
unsigned int recieverPort = 1885;
char packetBuffer[255];
EthernetUDP Udp;
int packetSize;


void moveUp(unsigned long steps){

  digitalWrite(DIR, HIGH);
  digitalWrite(ENA, HIGH);

  for (unsigned long i = 0; i < steps; i++){
    if(height >= max_height)
      return;

    digitalWrite(PUL, HIGH);
    delayMicroseconds(50);
    digitalWrite(PUL, LOW);
    delayMicroseconds(50);

    height += 1 / (double)stepmm;
  }
}


void moveDown(unsigned long steps){

  digitalWrite(DIR, LOW);
  digitalWrite(ENA, HIGH);

  for (unsigned long i = 0; i < steps; i++){
    if (digitalRead(microSwitchPin) == LOW)
      break;

    digitalWrite(PUL, HIGH);
    delayMicroseconds(50);
    digitalWrite(PUL, LOW);
    delayMicroseconds(50);
    height -= 1 / (double)stepmm;
  }
}


void calibrate(){
  // Go to bottom
  while (digitalRead(microSwitchPin) == HIGH)
     moveDown(1);

  // Go up 150 steps over switch trigger
  while (digitalRead(microSwitchPin) == LOW){
    for (int i = 0; i < 150; i++){
      moveUp(1);
    }
  }

  // Slowly go down until switch is triggered
  while (digitalRead(microSwitchPin) == HIGH){
    moveDown(1);
    delay(1);
  }

  height = 0;
}


void goTo(double millimeter){
  while (height < millimeter && height <= max_height)
    moveUp(1);
  
  while (height > millimeter && height >= 0)
    moveDown(1);
}

double getHeight(void){
  return height;
}


int main(void){

  init();
  pinMode(microSwitchPin, INPUT);
  pinMode(PUL, OUTPUT);
  pinMode(DIR, OUTPUT);
  pinMode(ENA, OUTPUT);
  Serial.begin(115200);

  //Get sender robot to 0 position
  calibrate();

  while (!Serial && millis() < 5000);

  Ethernet.init(SS_PIN);

  // Use Static IP and MAC
  byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0x0B };
  byte ip[] = {10, 132, 158, 192};
  Ethernet.begin(mac, ip);

  Udp.begin(localPort);

  char *command;
  char temp[100];
  double arg;
  
  for (;;){
    // if there's data available, read a packet
    packetSize = Udp.parsePacket();

    if (packetSize > 1){
      // read the packet into packetBufffer
      Udp.read(packetBuffer, 255);

      packetBuffer[packetSize] = '\0';

      //Split command and arg
      command = strtok(packetBuffer, ":");
      arg = String(strtok(NULL, ":")).toDouble();

      // Get command
      if (strcmp(command, "goTo") == 0){
        goTo(arg);

        Udp.beginPacket(Udp.remoteIP(), recieverPort);
        dtostrf(getHeight(), 3, 12, temp); //Convert double to char
        Udp.write(temp, strlen(temp));
        Udp.endPacket();

      }else if(strcmp(command, "moveDown") == 0){
        moveDown((unsigned long)arg);

        Udp.beginPacket(Udp.remoteIP(), recieverPort);
        dtostrf(getHeight(), 3, 12, temp); //Convert double to char
        Udp.write(temp, strlen(temp));
        Udp.endPacket();

      }else if(strcmp(command, "moveUp") == 0){
        moveUp((unsigned long)arg);

        Udp.beginPacket(Udp.remoteIP(), recieverPort);
        dtostrf(getHeight(), 3, 12, temp); //Convert double to char
        Udp.write(temp, strlen(temp));
        Udp.endPacket();

      }else{
        Udp.beginPacket(Udp.remoteIP(), recieverPort);
        Udp.write("Invalid command", strlen("Invalid command"));
        Udp.endPacket();
      }
    }

    if (serialEventRun) // Print whatever is not printed yet
      serialEventRun();
  }
  

  return 0;
}
