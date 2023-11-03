# Using the laser
## Setup
To use the laser simply connect the USB to the computer and take note of what port you connected to (on the raspberry pi it is usually /dev/ttyUSB0). You can then connect to the laser by calling the class:
``` python
from laser.optoNCDT1402 import optoNCDT1402

laser = optoNCDT1402("/dev/ttyUSB0")
```
This connects the laser to the computer via serial.
## Take measurements
To measure the distance with the laser, first make sure that it is on by connecting the laser off pin to ground then calling the measure() method:
``` python
from laser.optoNCDT1402 import optoNCDT1402

laser = optoNCDT1402("/dev/ttyUSB0")

distance = laser.measure()
```
This can easily be modified to takea measurement value every second:
``` python
from laser.optoNCDT1402 import optoNCDT1402
from time import sleep

laser = optoNCDT1402("/dev/ttyUSB0")
while True:
    distance = laser.measure()
    sleep(1)
```

## Get info and change moving average
Information about the laser can be recieved using getInfo():
``` python
from laser.optoNCDT1402 import optoNCDT1402

laser = optoNCDT1402("/dev/ttyUSB0")
print(laser.getInfo())
```
The internal moving average can also be changed by calling the setMovingAverage() method:
``` python
from laser.optoNCDT1402 import optoNCDT1402

laser = optoNCDT1402("/dev/ttyUSB0")
laser.setMovingAverage(10)
print(laser.getInfo())
```
The Filter Type should then read moving average and the Filter Number should read 10.

# optoNCDT1402-100 Class documentation
This document explains how to use the distance measurement sensor optoNCDT1402 and all of its functionalities.
The class needs the library pyserial 3.15. To install the library run the command
```
$ pip install pyserial
```
or the command
```
$ pip install -r requirements.txt
```
in the command prompt.

## Initialize class:
To initialize the class write optoNCDT1402() if the default parameters are correct. If not, the parameters comPort and noMeasurements can be added to the class call such that it becomes optoNCDT1402(comPort, noMeasurements).


### Parameters

**comPort:** A string with the name of the port on the computer the laser is connected to.

**noMeasurements:** The number of measurements to be averaged over before returning the distance. If you do not require averaging set it to 1 or leave it blank.
## Get laser info:
In the class you can retrieve the information stored in the laser. It will return in the form of a string and look something like

>ILD 1402: Standard <br> 
>A/N: 4120154 <br>
>O/N: 000 <br>
>S/N: 1234570 <br>
>MR: 50 <br>
>SoftVer: 1.001.796 <br> 
>BootVer: 1.001.16 <br>
>Date: 09/01/23 <br>
>Out Channel: analog | digital <br>
>Analog Error: last value | error value | error value after cycles xx //xx is 2 up to 99 <br>
>Filter Type: moving average | median<br>
>Filter Number: xx //with moving average xx is 1 up to 128, with median xx is 7, 5, 7 or 9<br>
>Scanrate: xxHz //xx is 1500 Hz, 1000 Hz, 750 Hz, 375 Hz<br> 
>type of digital output: binary | ascii <br>
>mode of analog/digital output: continuous | time | trigger<br>
>output time: xx //xx is time in ms 1<br>
>key status: unlock | lock | auto lock <br>
>mode of save setting: no save | save at each time<br> 
>mode of extern input: as teach in | as output trigger<br>
>peak searching: global maximum | first peak | last peak <br>
>Teach value 1: xx //xx is 1.0 up to 16368.0 <br>
>Teach value 2: xx //xx is 1.0 up to 16368.0<br>

To get the string, call optoNCDT1402.getInfo()

## Set moving average:
The laser have a function to set the Filter Type to moving average and the Filter Number. This means that a moving average of the last xx measurements are returned from the laser. This function can be set with the optoNCDT1402.setMovingAverage() call and returns True if it succeded or False if it did not. The parameter averagingNumber can be set to an integer to set the number of measurements to average over in the moving average.

### Parameters

**averagingNumber:** An int defining the number of measurements to average over in the laser

## Turn laser on/off:
The laser can be turned on or off from the class using the calls optoNCDT1402.laserOff() to turn off and optoNCDT1402.laserOn() to turn on. They both return True if it worked and False if it did not. The small black cable called laser_off needs to be grounded for the calls to work properly.

**The calls are volitile! The laser will always be on after disconnecting power!**

<span style = "color:red">**ALWAYS ASSUME THE LASER TO BE ON WHEN STARTING. DO NOT LOOK INTO THE LASER**</span>

## Get measurements:
To get measurements from the laser, call optoNCDT1402.measure(). This will start the measuring process by collecting two bytes from the laser and combining them to one difital number. The function then converts it to a distance in mm or an error string based on that digital number.

### Returns
Error or distance in mm
