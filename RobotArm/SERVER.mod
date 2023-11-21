MODULE SERVER

!////////////////
!GLOBAL VARIABLES
!////////////////

!//Robot configuration
PERS tooldata currentTool := [TRUE, [[0, 0, 0], [1, 0, 0, 0]],[0.001, [0, 0, 0.001],[1, 0, 0, 0], 0, 0, 0]];
PERS wobjdata currentWobj := [FALSE,TRUE,"",[[0,0,0],[1,0,0,0]],[[0,0,0],[1,0,0,0]]];    

PERS speeddata currentSpeed;
PERS zonedata currentZone;

!// Clock Synchronization
PERS bool startLog:=TRUE;
PERS bool startRob:=TRUE;

!// Mutex between logger and changing the tool and work objects
PERS bool frameMutex:=FALSE;

!//PC communication
VAR socketdev clientSocket;
VAR socketdev serverSocket;
VAR num instructionCode;
VAR num params{10};
VAR num nParams;

PERS string ipController:= "192.168.0.50"; !robot default IP
!PERS string ipController:= "127.0.0.1"; !local IP for testing in simulation
PERS num serverPort:= 5000;

!//Motion of the robot
VAR robtarget cartesianTarget;
VAR robtarget currentCartesianPose;
VAR jointtarget jointsTarget;
VAR bool moveCompleted; !Set to true after finishing a Move instruction.


!//Buffered move variables
CONST num MAX_BUFFER := 512;
VAR num BUFFER_POS := 0;
VAR robtarget bufferTargets{MAX_BUFFER};
VAR speeddata bufferSpeeds{MAX_BUFFER};

!//External axis position variables
VAR extjoint externalAxis;

!//Circular move buffer
VAR robtarget circPoint;

!//Correct Instruction Execution and possible return values
VAR num ok;
CONST num SERVER_BAD_MSG :=  0;
CONST num SERVER_OK := 1;

!//TCP data in relation to the end effector
PERS tooldata laser_TCP := [TRUE,[[-52,6.502,80.05],[1,0,0,0]],[0.1,[-29.004,-0.354,42.84],[1,0,0,0],0,0,0]];
PERS tooldata antenna_TCP := [TRUE,[[-54.5,36.262,94],[1,0,0,0]],[0.1,[-29.004,-0.354,42.84],[1,0,0,0],0,0,0]];
PERS tooldata calibration_laser_TCP := [TRUE,[[-62,-10.987,55.727],[0.707106781,0,-0.707106781,0]],[0.1,[-29.004,-0.354,42.84],[1,0,0,0],0,0,0]];
PERS tooldata calibration_antenna_TCP := [TRUE,[[-53.947,37.22,128],[1,0,0,0]],[0.1,[-29.004,-0.354,42.84],[1,0,0,0],0,0,0]];

!//Used to determine the x and y coordinates when determining the current zone of the TCP
VAR num x;
VAR num y;

!//When traveling to new zone it should pass through these points 
VAR robtarget cartesianTargetZone1 := [[141.4213562373095, 141.4213562373095, -150], [0.27059805, 0.65328148, 0.27059805, -0.65328148], [-1,0,0,4], [0.000004418,9E+09,9E+09,9E+09,9E+09,9E+09]];
VAR jointtarget targetZone1 := [[-90, -90, 15, -30, 110, 45], [45, 0, 0, 0 ,0 ,0]];

VAR robtarget cartesianTargetZone2 := [[-141.42135623730948, 141.4213562373095, -150], [0.65328148, 0.27059805, 0.65328148, -0.27059805], [0,0,0,4], [61.00,9E+09,9E+09,9E+09,9E+09,9E+09]];
VAR jointtarget targetZone2 := [[-43, -114, 20, 0, 95, 0], [0, 0, 0, 0 ,0 ,0]];

VAR robtarget cartesianTargetZone3 := [[-141.42135623730954, -141.42135623730948, -150], [0.65328148, -0.27059805, 0.65328148, 0.27059805], [1,0,0,4], [118.81,9E+09,9E+09,9E+09,9E+09,9E+09]];
VAR jointtarget targetZone3 := [[45, -115, 20, 0, 95, 0], [0, 0, 0, 0 ,0 ,0]];

VAR robtarget cartesianTargetZone4 := [[141.42135623730948, -141.42135623730954, -150], [-0.27059805, 0.65328148, -0.27059805, -0.65328148], [2,1,1,4], [156.144578313,9E+09,9E+09,9E+09,9E+09,9E+09]];
VAR jointtarget targetZone4 := [[80, -80, 10, 40, 120, -60], [-60, 0, 0, 0 ,0 ,0]];

!//Coordinate of the point the user wants to calibrate from
VAR robtarget calibrationCoordinate;

VAR robtarget resetPosition := [[-38.859585784,0.000707752,416.889532938],[0.53729967,-0.00000001,0.843391406,-0.000000007],[0,0,0,4],[90,9E+09,9E+09,9E+09,9E+09,9E+09]];

VAR robtarget currentZonePos;
VAR jointtarget newJointPos;

VAR robtarget newZonePos;
    

VAR num newZonePosID;

VAR num use_zones := 0;

	
!////////////////
!LOCAL METHODS
!////////////////

!//Method to parse the message received from a PC
!// If correct message, loads values on:
!// - instructionCode.
!// - nParams: Number of received parameters.
!// - params{nParams}: Vector of received params.
PROC ParseMsg(string msg)
    !//Local variables
    VAR bool auxOk;
    VAR num ind:=1;
    VAR num newInd;
    VAR num length;
    VAR num indParam:=1;
    VAR string subString;
    VAR bool end := FALSE;
	
    !//Find the end character
    length := StrMatch(msg,1,"#");
    IF length > StrLen(msg) THEN
        !//Corrupt message
        nParams := -1;
    ELSE
        !//Read Instruction code
        newInd := StrMatch(msg,ind," ") + 1;
        subString := StrPart(msg,ind,newInd - ind - 1);
        auxOk:= StrToVal(subString, instructionCode);
        IF auxOk = FALSE THEN
            !//Impossible to read instruction code
            nParams := -1;
        ELSE
            ind := newInd;
            !//Read all instruction parameters (maximum of 8)
            WHILE end = FALSE DO
                newInd := StrMatch(msg,ind," ") + 1;
                IF newInd > length THEN
                    end := TRUE;
                ELSE
                    subString := StrPart(msg,ind,newInd - ind - 1);
                    auxOk := StrToVal(subString, params{indParam});
                    indParam := indParam + 1;
                    ind := newInd;
                ENDIF	   
            ENDWHILE
            nParams:= indParam - 1;
        ENDIF
    ENDIF
ENDPROC


!//Handshake between server and client:
!// - Creates socket.
!// - Waits for incoming TCP connection.
PROC ServerCreateAndConnect(string ip, num port)
    VAR string clientIP;
	
    SocketCreate serverSocket;
    SocketBind serverSocket, ip, port;
    SocketListen serverSocket;
    TPWrite "SERVER: Server waiting for incoming connections ...";
    WHILE SocketGetStatus(clientSocket) <> SOCKET_CONNECTED DO
        SocketAccept serverSocket,clientSocket \ClientAddress:=clientIP \Time:=WAIT_MAX;
        IF SocketGetStatus(clientSocket) <> SOCKET_CONNECTED THEN
            TPWrite "SERVER: Problem serving an incoming connection.";
            TPWrite "SERVER: Try reconnecting.";
        ENDIF
        !//Wait 0.5 seconds for the next reconnection
        WaitTime 0.5;
    ENDWHILE
    TPWrite "SERVER: Connected to IP " + clientIP;
ENDPROC


!//Parameter initialization
!// Loads default values for
!// - Tool.
!// - WorkObject.
!// - Zone.
!// - Speed.
PROC Initialize()
    currentTool := [TRUE,[[0,0,0],[1,0,0,0]],[0.001,[0,0,0.001],[1,0,0,0],0,0,0]]; 
    currentWobj := [FALSE,TRUE,"",[[0,0,0],[1,0,0,0]],[[0, 0, 0],[1,0,0,0]]]; !Set to frame of OUS, currently hardcoded coordinates
    currentSpeed := [100, 50, 0, 0];
    currentZone := [FALSE, 0.3, 0.3,0.3,0.03,0.3,0.03]; !z0
	
	!Find the current external axis values so they don't move when we start
	jointsTarget := CJointT();
	externalAxis := jointsTarget.extax;
    
ENDPROC

!Find the current zone the tool is currently in
FUNC num zonePlacement()
    currentCartesianPose := CRobT(\WObj:=currentWObj);

    !Rounded to avoid misreading when coordinate close to 0
    x := round(currentCartesianPose.trans.x);
    y := round(currentCartesianPose.trans.y);

    IF x >= 0 AND y >= 0 THEN
        currentZonePos := cartesianTargetZone1;
        !currentZonePos := targetZone1;
        RETURN 1;

    ELSEIF x < 0 AND y >= 0 THEN
        currentZonePos := cartesianTargetZone2;
        !currentZonePos := targetZone2;
        RETURN 2;
    
    ELSEIF x < 0 AND y < 0 THEN
        currentZonePos := cartesianTargetZone3;
        !currentZonePos := targetZone3;
        RETURN 3;
    
    ELSE
        currentZonePos := cartesianTargetZone4;
        !currentZonePos := targetZone4;
        RETURN 4;
    
    ENDIF
ENDFUNC


!////////////////////////
!//SERVER: Main procedure
!////////////////////////
PROC main()
    !//Local variables
    VAR string receivedString;   !//Received string
    VAR string sendString;       !//Reply string
    VAR string addString;        !//String to add to the reply.
    VAR bool connected;          !//Client connected
    VAR bool reconnected;        !//Drop and reconnection happened during serving a command
    VAR robtarget cartesianPose;
    VAR jointtarget jointsPose;
        
    			
    !//Motion configuration
    ConfL \Off;
    ConfJ \Off;
    SingArea \Wrist;
    moveCompleted:= TRUE;
	
    !//Initialization of WorkObject, Tool, Speed and Zone
    Initialize;

    !//Socket connection
    connected:=FALSE;
    ServerCreateAndConnect ipController,serverPort;	
    connected:=TRUE;
    
    !//Server Loop
    WHILE TRUE DO
        !//Initialization of program flow variables
        ok:=SERVER_OK;              !//Correctness of executed instruction.
        reconnected:=FALSE;         !//Has communication dropped after receiving a command?
        addString := "";            

        !//Wait for a command
        SocketReceive clientSocket \Str:=receivedString \Time:=WAIT_MAX;
        ParseMsg receivedString;

        !//Execution of the command
        TEST instructionCode
            CASE 0: !Ping
                IF nParams = 0 THEN
                    ok := SERVER_OK;
                ELSE
                    ok := SERVER_BAD_MSG;
                ENDIF

            CASE 1: !Cartesian Move
                IF nParams = 7 THEN
                    
                    !Determine zone it currently is in and set correct joint parameters for the zone
                    IF params{1} >= 0 AND params{2} >= 0 THEN
                        newZonePosID := 1;
                        cartesianTarget:=[[params{1},params{2},params{3}],
                                           [params{4},params{5},params{6},params{7}],
                                           [-1,0,0,4],
                                           externalAxis];

                    ELSEIF params{1} < 0 AND params{2} >= 0 THEN
                        newZonePosID := 2;
                        cartesianTarget:=[[params{1},params{2},params{3}],
                                           [params{4},params{5},params{6},params{7}],
                                           [0,0,1,4],
                                           [61.00,9E+09,9E+09,9E+09,9E+09,9E+09]];

                    ELSEIF params{1} < 0 AND params{2} < 0 THEN
                        newZonePosID := 3;
                        cartesianTarget:=[[params{1},params{2},params{3}],
                                           [params{4},params{5},params{6},params{7}],
                                           [0,0,0,4],
                                           [118.81,9E+09,9E+09,9E+09,9E+09,9E+09]];
                    
                    ELSE
                        newZonePosID := 4;
                        cartesianTarget:=[[params{1},params{2},params{3}],
                                           [params{4},params{5},params{6},params{7}],
                                           [2,1,1,4],
                                           [156.144578313,9E+09,9E+09,9E+09,9E+09,9E+09]];
                    ENDIF
                    

                    ok := SERVER_OK;
                    moveCompleted := FALSE;
                    
                    !If coordinate is in different zone than the current zone
                    !Move through zones before move to target coordinate
                    
                    IF use_zones = 1 THEN

                        !Move up through the zones
                        IF newZonePosID > zonePlacement() THEN
                            MoveL currentZonePos, [100, 50, 50, 50], currentZone, currentTool \Wobj:=currentWobj;
                            WHILE newZonePosID > zonePlacement() DO                           
                                
                                IF zonePlacement() = 1 THEN
                                    newZonePos := cartesianTargetZone2;
                                    newJointPos := targetZone2;
                                
                                ELSEIF zonePlacement() = 2 THEN
                                    newZonePos := cartesianTargetZone3;
                                    newJointPos := targetZone3;
                                ELSE
                                    newZonePos := cartesianTargetZone4;
                                    newJointPos := targetZone4;
                                ENDIF
                                
                                MoveAbsJ newJointPos, [100, 50, 50, 50], currentZone, currentTool \Wobj:=currentWobj;
                                !MoveL newZonePos, [100, 50, 50, 50], currentZone, currentTool \WObj:=currentWobj;
                            ENDWHILE
                        
                        !Move down through the zones
                        ELSEIF newZonePosID < zonePlacement() THEN
                            MoveL currentZonePos, [100, 50, 50, 50], currentZone, currentTool \Wobj:=currentWobj;
                            
                            WHILE newZonePosID < zonePlacement() DO
                                
                                
                                IF zonePlacement() = 4 THEN
                                    newZonePos := cartesianTargetZone3;
                                    newJointPos := targetZone3;
                                    
                                ELSEIF zonePlacement() = 3 THEN
                                    newZonePos := cartesianTargetZone2;
                                    newJointPos := targetZone2;
                                ELSE
                                    newZonePos := cartesianTargetZone1;
                                    newJointPos := targetZone1;
                                ENDIF
                                MoveAbsJ newJointPos, [100, 50, 50, 50], currentZone, currentTool \Wobj:=currentWobj;
                                !MoveL newZonePos, [100, 50, 50, 50], currentZone, currentTool \WObj:=currentWobj;
                            ENDWHILE
                            
                        ENDIF
                    ENDIF


                    MoveL cartesianTarget, currentSpeed, currentZone, currentTool \WObj:=currentWobj;
                    moveCompleted := TRUE;
                ELSE
                    ok := SERVER_BAD_MSG;
                ENDIF	
				
            CASE 2: !Joint Move
                IF nParams = 7 THEN
                    externalAxis := [params{7},0,0,0,0,0];
                    jointsTarget:=[[params{1},params{2},params{3},params{4},params{5},params{6}], externalAxis]; 
                    ok := SERVER_OK;
                    moveCompleted := FALSE;
                    MoveAbsJ jointsTarget, currentSpeed, currentZone, currentTool \Wobj:=currentWobj;
                    moveCompleted := TRUE;
                ELSE
                    ok :=SERVER_BAD_MSG;
                ENDIF

            CASE 3: !Get Cartesian Coordinates (with current tool and workobject)
                IF nParams = 0 THEN
                    cartesianPose := CRobT(\Tool:=currentTool \WObj:=currentWObj);		
                    addString := NumToStr(cartesianPose.trans.x,2) + " ";
                    addString := addString + NumToStr(cartesianPose.trans.y,2) + " ";
                    addString := addString + NumToStr(cartesianPose.trans.z,2) + " ";
                    addString := addString + NumToStr(cartesianPose.rot.q1,3) + " ";
                    addString := addString + NumToStr(cartesianPose.rot.q2,3) + " ";
                    addString := addString + NumToStr(cartesianPose.rot.q3,3) + " ";
                    addString := addString + NumToStr(cartesianPose.rot.q4,3); !End of string	
                    ok := SERVER_OK;
                ELSE
                    ok :=SERVER_BAD_MSG;
                ENDIF

            CASE 4: !Get Joint Coordinates
                IF nParams = 0 THEN
                    jointsPose := CJointT();
                    addString := NumToStr(jointsPose.robax.rax_1,2) + " ";
                    addString := addString + NumToStr(jointsPose.robax.rax_2,2) + " ";
                    addString := addString + NumToStr(jointsPose.robax.rax_3,2) + " ";
                    addString := addString + NumToStr(jointsPose.robax.rax_4,2) + " ";
                    addString := addString + NumToStr(jointsPose.robax.rax_5,2) + " ";
                    addString := addString + NumToStr(jointsPose.robax.rax_6,2) + " ";
                    addString := addString + NumToStr(jointsPose.extax.eax_a,2); !End of string
                    ok := SERVER_OK;
                ELSE
                    ok:=SERVER_BAD_MSG;
                ENDIF
			CASE 5: !Get external axis positions
                IF nParams = 0 THEN
                    jointsPose := CJointT();
                    addString := NumToStr(jointsTarget.extax.eax_a, 2) + " ";
                    !addString := addString + StrPart(NumToStr(jointsTarget.extax.eax_b,2),1,8) + " ";
                    !addString := addString + StrPart(NumToStr(jointsTarget.extax.eax_c,2),1,8) + " ";
                    !addString := addString + StrPart(NumToStr(jointsTarget.extax.eax_d,2),1,8) + " ";
                    !addString := addString + StrPart(NumToStr(jointsTarget.extax.eax_e,2),1,8) + " ";
                    !addString := addString + StrPart(NumToStr(jointsTarget.extax.eax_f,2),1,8); !End of string
                    ok := SERVER_OK;
                ELSE
                    ok:=SERVER_BAD_MSG;
                ENDIF	
		
            CASE 6: !Set Tool
                IF nParams = 7 THEN
		            WHILE (frameMutex) DO
		                WaitTime .01; !// If the frame is being used by logger, wait here
		            ENDWHILE
		            frameMutex:= TRUE;
                    currentTool.tframe.trans.x:=params{1};
                    currentTool.tframe.trans.y:=params{2};
                    currentTool.tframe.trans.z:=params{3};
                    currentTool.tframe.rot.q1:=params{4};
                    currentTool.tframe.rot.q2:=params{5};
                    currentTool.tframe.rot.q3:=params{6};
                    currentTool.tframe.rot.q4:=params{7};
                    ok := SERVER_OK;
		            frameMutex:= FALSE;
                ELSE
                    ok:=SERVER_BAD_MSG;
                ENDIF

            CASE 7: !Set Work Object
                IF nParams = 7 THEN
                    currentWobj.oframe.trans.x:=params{1};
                    currentWobj.oframe.trans.y:=params{2};
                    currentWobj.oframe.trans.z:=params{3};
                    currentWobj.oframe.rot.q1:=params{4};
                    currentWobj.oframe.rot.q2:=params{5};
                    currentWobj.oframe.rot.q3:=params{6};
                    currentWobj.oframe.rot.q4:=params{7};
                    ok := SERVER_OK;
                ELSE
                    ok:=SERVER_BAD_MSG;
                ENDIF

            CASE 8: !Set Speed of the Robot
                IF nParams = 4 THEN
                    currentSpeed.v_tcp:=params{1};
                    currentSpeed.v_ori:=params{2};
                    currentSpeed.v_leax:=params{3};
                    currentSpeed.v_reax:=params{4};
                    ok := SERVER_OK;
                ELSEIF nParams = 2 THEN
					currentSpeed.v_tcp:=params{1};
					currentSpeed.v_ori:=params{2};
					ok := SERVER_OK;
				ELSE
                    ok:=SERVER_BAD_MSG;
                ENDIF

            CASE 9: !Set zone data
                IF nParams = 4 THEN
                    IF params{1}=1 THEN
                        currentZone.finep := TRUE;
                        currentZone.pzone_tcp := 0.0;
                        currentZone.pzone_ori := 0.0;
                        currentZone.zone_ori := 0.0;
                    ELSE
                        currentZone.finep := FALSE;
                        currentZone.pzone_tcp := params{2};
                        currentZone.pzone_ori := params{3};
                        currentZone.zone_ori := params{4};
                    ENDIF
                    ok := SERVER_OK;
                ELSE
                    ok:=SERVER_BAD_MSG;
                ENDIF

            CASE 10: !Unlock joint, NOT currently implemented
        
                ok := SERVER_OK;
                moveCompleted := FALSE;
                MoveL resetPosition, currentSpeed, currentZone, laser_TCP \WObj:=currentWobj;
                moveCompleted := TRUE;

            CASE 11: !Set current coordinates as new workspace
                IF nParams = 0 THEN
                    calibrationCoordinate := CRobT(\Tool:=calibration_antenna_TCP \WObj:=currentWObj);
                    currentWobj.oframe.trans.x := calibrationCoordinate.trans.x;
                    currentWobj.oframe.trans.y := calibrationCoordinate.trans.y;
                    currentWobj.oframe.trans.z := calibrationCoordinate.trans.z;
                    currentWobj.oframe.rot.q1 := 1;
                    currentWobj.oframe.rot.q2 := 0;
                    currentWobj.oframe.rot.q3 := 0;
                    currentWobj.oframe.rot.q4 := 0;
                    ok := SERVER_OK;
                ELSE
                    ok:=SERVER_BAD_MSG;
                ENDIF

            CASE 12: !Change the current TCP tool
                IF nParams = 1 THEN
                    IF params{1} = 1 THEN
                        currentTool := laser_TCP;
                    ELSE
                        currentTool := antenna_TCP;
                    ENDIF
                ELSE
                    ok:=SERVER_BAD_MSG;
                ENDIF
            

            CASE 13: !Set zone traversement
                IF nParams = 1 THEN
                    IF params{1} = 1 THEN
                        use_zones := 1;
                    ELSE
                        use_zones := 0;
                    ENDIF
                ELSE
                    ok:=SERVER_BAD_MSG;
                ENDIF
            

            CASE 30: !Add Cartesian Coordinates to buffer
                IF nParams = 7 THEN
                    cartesianTarget :=[[params{1},params{2},params{3}],
                                        [params{4},params{5},params{6},params{7}],
                                        [0,0,0,0],
                                        externalAxis];
                    IF BUFFER_POS < MAX_BUFFER THEN
                        BUFFER_POS := BUFFER_POS + 1;
                        bufferTargets{BUFFER_POS} := cartesianTarget;
                        bufferSpeeds{BUFFER_POS} := currentSpeed;
                    ENDIF
                    ok := SERVER_OK;
                ELSE
                    ok:=SERVER_BAD_MSG;
                ENDIF

            CASE 31: !Clear Cartesian Buffer
                IF nParams = 0 THEN
                    BUFFER_POS := 0;	
                    ok := SERVER_OK;
                ELSE
                    ok:=SERVER_BAD_MSG;
                ENDIF

            CASE 32: !Get Buffer Size)
                IF nParams = 0 THEN
                    addString := NumToStr(BUFFER_POS,2);
                    ok := SERVER_OK;
                ELSE
                    ok:=SERVER_BAD_MSG;
                ENDIF

            CASE 33: !Execute moves in cartesianBuffer as linear moves
                IF nParams = 0 THEN
                    FOR i FROM 1 TO (BUFFER_POS) DO 
                        MoveL bufferTargets{i}, bufferSpeeds{i}, currentZone, currentTool \WObj:=currentWobj ;
                    ENDFOR			
                    ok := SERVER_OK;
                ELSE
                    ok:=SERVER_BAD_MSG;
                ENDIF

            CASE 34: !External Axis move
                IF nParams = 6 THEN
                    externalAxis :=[params{1},params{2},params{3},params{4},params{5},params{6}];
                    jointsTarget := CJointT();
                    jointsTarget.extax := externalAxis;
                    ok := SERVER_OK;
                    moveCompleted := FALSE;
                    MoveAbsJ jointsTarget, currentSpeed, currentZone, currentTool \Wobj:=currentWobj;
                    moveCompleted := TRUE;
                ELSE
                    ok :=SERVER_BAD_MSG;
                ENDIF

            CASE 35: !Specify circPoint for circular move, and then wait on toPoint
                IF nParams = 7 THEN
                    circPoint :=[[params{1},params{2},params{3}],
                                [params{4},params{5},params{6},params{7}],
                                [0,0,0,0],
                                externalAxis];
                    ok := SERVER_OK;
                ELSE
                    ok:=SERVER_BAD_MSG;
                ENDIF

            CASE 36: !specify toPoint, and use circPoint specified previously
                IF nParams = 7 THEN
                    cartesianTarget :=[[params{1},params{2},params{3}],
                                        [params{4},params{5},params{6},params{7}],
                                        [0,0,0,0],
                                        externalAxis];
                    MoveC circPoint, cartesianTarget, currentSpeed, currentZone, currentTool \WObj:=currentWobj ;
                    ok := SERVER_OK;
                ELSE
                    ok:=SERVER_BAD_MSG;
                ENDIF
				
            CASE 98: !returns current robot info: serial number, robotware version, and robot type
                IF nParams = 0 THEN
                    addString := GetSysInfo(\SerialNo) + "*";
                    addString := addString + GetSysInfo(\SWVersion) + "*";
                    addString := addString + GetSysInfo(\RobotType);
                    ok := SERVER_OK;
                ELSE
                    ok :=SERVER_BAD_MSG;
                ENDIF
			
            CASE 99: !Close Connection
                IF nParams = 0 THEN
                    TPWrite "SERVER: Client has closed connection.";
                    connected := FALSE;
                    !//Closing the server
                    SocketClose clientSocket;
                    SocketClose serverSocket;

                    !Reinitiate the server
                    ServerCreateAndConnect ipController,serverPort;
                    connected := TRUE;
                    reconnected := TRUE;
                    ok := SERVER_OK;
                ELSE
                    ok := SERVER_BAD_MSG;
                ENDIF
            DEFAULT:
                TPWrite "SERVER: Illegal instruction code";
                ok := SERVER_BAD_MSG;
        ENDTEST
		
        !Compose the acknowledge string to send back to the client
        IF connected = TRUE THEN
            IF reconnected = FALSE THEN
			    IF SocketGetStatus(clientSocket) = SOCKET_CONNECTED THEN
				    sendString := NumToStr(instructionCode,0);
                    sendString := sendString + " " + NumToStr(ok,0);
                    sendString := sendString + " " + addString;
                    SocketSend clientSocket \Str:=sendString;
			    ENDIF
            ENDIF
        ENDIF
    ENDWHILE

    ERROR (LONG_JMP_ALL_ERR)
    TPWrite "SERVER: ------";
    TPWrite "SERVER: Error Handler:" + NumtoStr(ERRNO,0);
    TEST ERRNO
        CASE ERR_SOCK_CLOSED:
            TPWrite "SERVER: Lost connection to the client.";
            TPWrite "SERVER: Closing socket and restarting.";
            TPWrite "SERVER: ------";
            connected:=FALSE;
            !//Closing the server
            SocketClose clientSocket;
            SocketClose serverSocket;
            !//Reinitiate the server
            ServerCreateAndConnect ipController,serverPort;
            reconnected:= FALSE;
            connected:= TRUE;
            RETRY; 
        DEFAULT:
            TPWrite "SERVER: Unknown error.";
            TPWrite "SERVER: Closing socket and restarting.";
            TPWrite "SERVER: ------";
            connected:=FALSE;
            !//Closing the server
            SocketClose clientSocket;
            SocketClose serverSocket;
            !//Reinitiate the server
            ServerCreateAndConnect ipController,serverPort;
            reconnected:= FALSE;
            connected:= TRUE;
            RETRY;
    ENDTEST
ENDPROC

ENDMODULE

