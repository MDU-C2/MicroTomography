# Robot Arm documentation - IRB 14050 Single Arm YuMi
This document is for information regarding the robotarm.

## Upload script to YuMi robot arm:
Currently a slightly modified script of *SERVER.mod* is used , which can be found at https://github.com/robotics/open_abb. The modification done was from
*PERS string ipController:= "127.0.0.1";*
to
*PERS string ipController:= "192.168.0.100";* (the IP address will vary depending the on the address it is given by the DHCP server)

To upload the script to the YuMi controller you need RobotStudio. Ensure you are either:

* Connected to the YuMi via the MGMT port and that your PC has an IP address of 192.168.125.[2-254]. YuMi has an IP address of 192.168.125.1 which is static. Check connection from PC by opening a terminal and type "*ping 192.168.125.1*". If connection is established ping will be successful.
* Or connect the YuMi and your PC to a router that supports DHCP. When connecting the YuMi to router, use the WAN port on the YuMi. Find the allocated IP address of the YuMi by navigating to Settings -> Network settings on the YuMi FlexPendant. Check connection from PC by opening a terminal and ping the IP address found on the FlexPendant.

When connection has been established, open RobotStudio:
1. File -> Online -> One Click Connect
2. Open tab RAPID -> Program -> Load Module, upload "*SERVER.mod*". This will upload the module to the YuMi controller.
3. On the FlexPendant, navigate to *Operate*, select the uploaded file and press the physical *Play button* on the FlexPendant 




## Joints range of motion:

| Joint     | Range (degrees)   |
| --------  | -------           |
| 1         | (-168.5) - 168.5  |
| 2         | (-143.51) - 43.49 |
| 3         | (-123.5) - 79.96  |
| 4         | (-289.95) - 289.84|
| 5         | (-87.62)  - 137.95|
| 6         | (-228.71) - 228.72|
| 7         | (-168.35) - 168.23|


## Get access to School licenses for RobotStudio (remove??) 
To get access for a school license of *RobotStudio* ensure you are connected to *eduroam* and perform the following steps in *RobotStudio*:

1. Navigate to **Options**
2. In **General**, navigate to **Licensing**
3. Press **Activation Wizard**
4. Press **Network License - I want to specify a network license server or manage server licenses** 
5. Enter the following IP address: *10.132.178.233*
6. *RobotStudio* will restart and to confirm the license is activated you can repeat Step 1-2 and then press **My Licenses** 

## How to simulate the *IRB 14050 - YuMi* in *RobotStudio*
This section describes how the robot arm can be simulated in *RobotStudio* which is a preferable initial step for programming and testing the robot arm. To simulate the robot arm, open *RobotStudio* and perform the following steps:

1. Create a new project by *File -> New -> Station*.
2. Create a new virtual controller by *Home -> Virtual Controller -> New Controller*
3. Select the *IRB 14050 0.5kg 0.5m* as the **Robot model** and choose the latest **RobotWare**. You can leave the rest unchanged, change the **Location** if you want to save the new controller in a different location than the default location.
4. When a pop-up window appears, select *IRB14050_0.5_0.5__03* and press **OK**.
5. To upload *RAPID* code to the virtual controller navigate to *RAPID -> Program -> Load Module* and upload the *RAPID* code you wish to execute. If you receive Errors after you have uploaded the code it might be due to there existing to *MAIN* files. In the tree structure to the left remove any *RAPID* files which you have not uploaded. To check if any errors persist press *RAPID -> Check Program* and check the log.
6. To start the simulation navigate to *Simulation -> Play*. *Do note that the simulation will not start if errors exist in the code. 
7. If you are sending commands to the robot arm via socket communication like this project. Ensure that the IP address in the *RAPID* and *Python* code are set to *127.0.0.1*  



## Potential issues and how to solve them
This section is for listing issues that has occured during the use of the arm whilst working with it during this project. Find potential issues here and how they were solved.

### Socket error 
If the FlexPendant reports that you have a socket connection error which prevents you from connecting to the socket, the internal firewall of the Controller might be blocking it. This error may occur if you factory reset the controller. To fix the issue, try the following.

1. Connect your PC to the MGMT port of the controller and change your IP address to an address in the following range *192.168.125.[2-254]*
2. Open *RobotStudio* and connect to the controller as specified in Section: **Upload script to YuMi robot arm**.
3. In *RobotStudio* open *Controller -> Configuration -> Communication*. Open the tab *Firewall* and ensure that the desrired connections are allowed through Firewall. After changes are applied controller needs to be restarted for the changes to be applied. 