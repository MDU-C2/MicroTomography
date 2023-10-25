To set up the system:
	The OUS must be in the middle of the USER FRAME (wBreast).
	
	How:
	- Set up the bench without the OUS
	- In jogging: 
		-Choose tLaser as the tool
		-Move the tool in front of the robot, pointing upwards.
		-use the align button to make sure the tool is pointing straight uppwards
		-Jog the robot to position x=0 and y=0 and z>0
	- Now: move the bench until the laser points in the middle of the hole that should hold the OUS


	Now the OUS will hang in the center of the USER FRAME 



Move the robot to a "good" position before starting the program.
The program:
	Start the proc Main().
	- The robot will first move to the Start position. It is supposed to find its way to the start position from any "normal" position.
	- Then, it attempts to connect to MATLAB.
	- The program then starts:
		-Get position from Matlab (included tool and speed)
		-Move to that position
		-Sends it position back to Matlab



*OUS = Object Under Detection (The breast model)



PROC in the code:
	main()
		The main code.
	
	connectmatlab()
		connects the Robot with MATLAB.

	MoveToStartPosition(num dist)
		Moves the robot from "any" (almost any normal positions for this application) to the start position. 
		-dist: the distance from the center of OUS

	GetAndMoveToNewPosition()
		This Proc will receive a position from MATLAB, and move to that position.

	SendCurrentPosition()
		This Proc will send the current position of the tool to MATLAB

	move(pos trans,num rotx,num roty,num rotz)
		This Proc will move the tool from the current position, to the position decided from MATLAB.
		-trans: trans of position to move to 
		-rotx: rotx of position to move to 
		-roty: roty of position to move to 
		-rotz: rotz of position to move to 

	MoveCirc(robtarget tStartPos,robtarget tDistGoalPos,num zrot,num goalDegree,num degreeStep)
		This Proc creates the circle movements from one Start Position towards the Goal position. 
    		The circle will be around the OUS with a distance = standardDist. The tool will allways point to the center of the OUS.
		-tStartPos: current position
		-tDistGoalPos: the last position in the circle to move to
		-zrot: current degree in the spherical coordinate system
		-goalDegree: The degrees of the last position in the circle
		-degreeStep: The degrees to move in one scoope
	

FUNC in the code:

	robtarget calcPosWithDistance(robtarget posisiton)
		calculate new position, from the position, with a distance (standard distance) from the breast center point. 
		The new position will have the same angle as the current position in the spherical coordinate system, but with the "standard distance" from the center of the OUS.
		-position: the position that is used to calculate a new position with a distance

	num calcTeta(robtarget posisiton)
		calculate the angle "teta". "teta" is the angel needed to calculate the x and y of the position in the circle, and also the angle we get from x and y. 
		-position: the position used to calc teta

	num TetaToDegree(num teta,robtarget posisiton)
		Using the angle "teta" to calculate the degrees in the spherical coordinate system.
		position: position used to calculate degrees
		-teta: teta of the position

	num degreeToTeta(num degree)
   		Using the degrees in the spherical coordinate system to calculate "teta". "teta" is the angel needed to calculate the x and y of the position in the circle, and also the angle we get from x and y. 
		-degree: degrees used to calculate teta

	string Send(string c)
		Send a string with the position of the tool to MATLAB
		-c: string with information to send

	string receive()
		receive a string with the position, tool and speed from MATLAB.

	robtarget goalposition(pos trans,num rotx,num roty,num rotz)
		Goalposition = the position the robot is moving towards. 
    		We have the trans and the root at that position, and this function create the robtarget that fits that position (conf and rotation of joint 7)
		-trans: trans of position of goal position
		-rotx: rotx of position of goal position
		-roty: roty of position of goal position
		-rotz: rotz of position of goal position
	
	num JointSpecificData(num joint)
		Gives back the rotation of a joint:
		-joint: the joint to calc degrees on 