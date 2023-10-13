# Robot Arm documentation
This document is for information regarding the robotarm.

## Upload script to YuMi robot arm:
Currently a slightly modified script of *SERVER.mod* is used , which can be found at https://github.com/robotics/open_abb. The modification done was from
*PERS string ipController:= "127.0.0.1";*
to
*PERS string ipController:= "192.168.0.100";* (the IP address will vary depending the on the address it is given by the DHCP server)

To upload the script to the YuMi controller you need RobotStudio. Ensure you are either:

* Connected to the YuMi via the MGMT port and that your PC has an IP address of 192.168.125.[2-255]. YuMi has an IP address of 192.168.125.1 which is static. Check connection from PC by opening a terminal and type "*ping 192.168.125.1*". If connection is established ping will be successful.
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