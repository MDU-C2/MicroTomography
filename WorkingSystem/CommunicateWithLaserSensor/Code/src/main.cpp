/****************************************************************************************************************************
  main.cpp

  This code is inspired and built upon UDPSendReceive.ino by Khoi Hoang https://github.com/khoih-prog/Ethernet_Generic

  It allows the Arduino to read data from the sensor and send and reqieve data over UDP

  The Arduino board communicates with the shield using the SPI bus. This is on digital pins 11, 12, and 13 on the Uno pin 10 is used as SS.

  Author: Emanuel Bjurhager
 *****************************************************************************************************************************/

#include "Ethernet_Generic.h"

#define SS_PIN 10

unsigned int localPort = 1000;
unsigned int recieverPort = 1884;

char packetBuffer[255];

EthernetUDP Udp;

char incoming[64];

int readLen;

int ConvertedValue;

unsigned int i;
unsigned int j;
unsigned int k;

int EN = 2; // Definition RS485 shield enable terminal (the 2nd digital IO ports),
            // high for the sending state, the low level of receiving state

void setup()
{
  Serial.begin(115200);
  pinMode(EN, OUTPUT);

  while (!Serial && millis() < 5000)
    ;

  Ethernet.init(SS_PIN);

  // Use Static IP and MAC
  byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xBE, 0x0A};
  byte ip[] = {10, 132, 158, 190};
  Ethernet.begin(mac, ip);

  Udp.begin(localPort);

  digitalWrite(EN, LOW); // Enable RX of serial shield
}

long temp;

void loop()
{
  // if there's data available, read a packet
  int packetSize = Udp.parsePacket();

  if (packetSize)
  {
    // read the packet into packetBufffer
    Udp.read(packetBuffer, 255);

    // Get command
    if (strcmp(packetBuffer, "Get") == 0)
    {
      if (Serial.available() > 16) // read 10 bytes. Less produces errors, more gives us more data to remove. 10 seem to be a "magic" number.
      {

        readLen = Serial.readBytes(incoming, 16);
        incoming[readLen + 1] = '\0';

        // Remove everything before the first \r
        for (i = 0; i < strlen(incoming); i++)
        {
          if (incoming[i] == '\r')
          {
            for (j = 0; j <= i; j++)
            {
              incoming[j] = ' ';
            }
            break;
          }
        }

        // Remove everything after the new first \r
        for (i = 0; i < strlen(incoming); i++)
        {
          if (incoming[i] == '\r')
          {
            for (j = i; j < strlen(incoming); j++)
            {
              incoming[j] = ' ';
            }
            break;
          }
        }

        // Remove all spaces before the number
        k = 0;
        for (i = 0; i < strlen(incoming); i++)
        {
          if (incoming[i] != ' ')
          {
            incoming[k] = incoming[i];
            k++;
          }
        }
        incoming[k] = '\0';

        // Send data
        Udp.beginPacket(Udp.remoteIP(), recieverPort);
        Udp.write(incoming, strlen(incoming));
        Udp.endPacket();
      }
    }
  }
}
