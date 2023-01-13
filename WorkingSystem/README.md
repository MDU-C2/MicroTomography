# MicroTomographyHT2022
This folder contains a working system that can communicate with both the receiver (SAY) and sender robot and the laser sensor. The system works the best when the setup is covered (we covered it with a blanket) to reduce noise from the enviroment. 

#To start the system:
1. Navigate into the GUI folder
2. Start the AppMainLayout matlab app (works with MATLAB R2022b)
3. Run the app
4. Make sure robot and laser are on
5. Press the "-" on the flex pendant which is included with the SAY
6. Press the play button (">") on the flex pendant to get the SAY ready for connection
7. Once the SAY has stopped moving press the "Connect to robot" button in the GUI app
8. When the status message in the log window states that its connected to the robot, press the "Scan model" button. The System will initiate a scanning process that can take some time.


*note*
All files in this folder might not be necessary for successful execution of the system. Some files could be artifacts and excess.