#MicroTomographyHT2022
In this repository you find a complete positioning and scanning system for the Microwave tomography project at MDU. The project was conducted in the fall/winter of 2022. 

Documentation of the project can be found in the documentation folder. Each subsystem has received their own folder. The complete, executable system, is found in the "WorkingSystem" folder.
Setup instructions for the SAY can be found in the "RAPID-SAY" folder's readme. Many of the subsystems can be tested individually, or have experimental code that is not included in the working system, therefore they have received their own folders, even if they are also included in the "WorkingSystem" folder.

#To start the full system:
1. Navigate into Working system folder then the GUI folder
2. Start the AppMainLayout matlab app (works with MATLAB R2022b)
3. Run the app
4. Make sure robot and laser are on
5. Press the "-" on the flex pendant which is included with the SAY
6. Press the play button (">") on the flex pendant to get the SAY ready for connection
7. Once the SAY has stopped moving press the "Connect to robot" button in the GUI app
8. When the status message in the log window states that its connected to the robot, press the "Scan model" button. The System will initiate a scanning process that can take some time.
