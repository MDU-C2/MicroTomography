# Microwave Imaging

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Install python packages from requirements.txt

Run the command

```console
pip install -r requirements.txt
```

In the command prompt

# Setup
First, make sure the following is powered on and set up as described.
## Router
- Connect the router to the eduroam network using an ethernet cable from the wall to the router.
- Connect the Raspberry Pi to the router using an ethernet cable.
- Connect the Network analyzer to the router using an ethernet cable.
- Connect the robot controller to the ruter using an ethernet cable.
- Power on the router by connecting it to a power outlet.

## Raspberry Pi 4
Set up the Raspberry pi:
- Connect the screen to the Pi using a micro-HDMI to HDMI cable.
- Connect the mouse and keyboard to the Pi using the USB-A conncetions.
- Connect a ethernet cable from the raspberry Pi to the router.
- Connect the USB-A side of the laser connection to a USB-A port on the Raspberry Pi
- Power on the Raspberry Pi by connecting the USB-C side of a Raspberry Pi 4 adapter to the Raspberry pi and the other side to a power outlet.

## Network Analyzer
- Connect the Microwave applicator to channel 2 on the network analyzer.
- Connect the Microwave reciever to channel 3 on the network analyzer.
- Connect the Lan 1 port of the network analyzer to the router using a ethernet cable.
- Conncet the power cable from the network analyzer to a power outlet.
- Make sure the switch by the power input is fliped to the on state.
- Power on the network analyser by pressing the on button in the lower left corner of the front panel. 

## Robot controller
- Connect the robot controller to the router using an ethernet cable.
- Connect a power cable from the robot controller to a power outlet.
- Power on the robot controller.

# Starting the program
There are two program to run. One is a terminal program and the other is a GUI, however, both lets you use the whole system. Both are located in the folder repositories/MicroTomography.

## Starting the terminal program
To start the terminal program follow these simple steps.
1. Follow the setup described above.
2. Locate the repositories/MicroTomography folder in the raspberry pi 4. This can be done by opening a new terminal window and typing `cd repositories/MicroTomography`.
3. Start the program main.py by typing `python3.10 main.py` in the terminal window.

## Starting the GUI
To start the GUI follow these simple steps.
1. Follow the setup described above.
2. Locate the repositories/MicroTomography folder in the raspberry pi 4. This can be done by opening a new terminal window and typing `cd repositories/MicroTomography`.
3. Start the program main.py by typing `python3.10 MainProgram.py` in the terminal window.


# Move linear actuator and take measurements
To only move the linear actuator and take measurements at the current configuration of the robot run the file *take_measurements.py* where you get a prompt asking what you want to do. It saves the microwave data in both s2p and csv format.
