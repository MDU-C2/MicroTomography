"# OrphanBranch2023 - GUI"  
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Here is for the GUI for the system. The red point represent the position of laser.

2023-09-27 Update:
It shows a table. The items in the table are the position for where the robot move.

It is able to insert the item to the table.

Show the matplotlib toolbox. 

Create a prototype scan button. It is read the data in the table and plot it. 

If the item in the table are not a number, then auto break the scanning

Add a “clear” button for clean “my list” table

Modifier some code 

Need to fix: 

The plot cannot draw the position of the laser continuous. 

Stop button.

2023-09-26 Update: 
It is able to save csv file

It is able to move the laser position with button under robotic arm movement

It is able to display log in the log window
                   
Disable stop and save button. Save button enable only when people had load a model

Minor code changes

2023-09-25 Update: 
It is able to load csv file and plot the point cloud now

![GUI_ver 1 1](https://github.com/MDU-C2/MicroTomography/assets/144024751/57e4b112-7a22-40ac-b46e-ff138bea6870)

File description:

ScanningSystem_ver_1.0.ui: A file made from pyQt5 designer

ScanningSystem.py: A python code file that convert from ScanningSystem_ver_1.0.ui

Button_LOAD.py: Code for load file 

Button_SAVE.py: Code for save file

app.py: code for the main program (you should run it for open the GUI)

testCSV.csv: A csv file made from Data\SurfacePoint11231426_NecCodeEm.mat from pervious work. It is use for test to print the points cloud.

readme.txt: Some information about the system
