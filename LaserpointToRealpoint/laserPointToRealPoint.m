clc
clear
close all;

<<<<<<< Updated upstream
laserlength=10;
posRobot=[-100,0,0];
rot=[0,90,0];

position = findSurfacePosition(rot,posRobot,laserlength);
=======
laserlength=100;

t = tcpclient('192.168.125.1',55000);
%disp (t.NumBytesAvailable)
flush (t);

a=[[0,0,100];[0,-100,50];[0,0,-100];[0,100,50]];
i=1;
while true
    %sendposition
    packAndSendPose(0, a(i,:), [0,0,0], t);
    i=i+1;

    if i>4
        i=1;
    end

    [pos, rot] = ReceiveAndUnpackPose(0, t);
    %posRobot=[-100,0,0];
    %rot=[0,90,0];
    disp('Rob Rot: ')
    disp(rot)
    disp('Rob Pos: ')
    disp(pos)
    scatter3(pos(1),pos(2),pos(3),'filled');
    hold on;
    position = findSurfacePosition(rot,pos,laserlength);
    scatter3(position(1),position(2),position(3));
    pause(.1);
    hold on;
end

>>>>>>> Stashed changes

function position = findSurfacePosition(rot,posRobot,laserlength)
    d=[0,0,0];
    laserlength=[0;0;laserlength;1];
    %disp('RobPos: ')
    %disp(posRobot)

    T1=createTransformationMatrix(rotx(rot(1)),posRobot);
    T2=createTransformationMatrix(roty(rot(2)),d);
    T3=createTransformationMatrix(rotz(rot(3)),d);
    T = T1*T2*T3;

    position = T*laserlength;
    position=position(1:3);

    disp('position Pos: ');
    disp(position)


end

function T=createTransformationMatrix(R,D)
<<<<<<< Updated upstream
    D=D';
    T = [R D];
    T = [T ; [0,0,0,1]];
end
=======

    D=D';

    T = [R D];
    T = [T ; [0,0,0,1]];
end

function [trans, rot] = ReceiveAndUnpackPose(~, t)

    %app.waitingOnPos = 1;
    %wait until message is received
    noMsgReceived = 1;
    while noMsgReceived
        receivedMsg = char(read(t));
        noMsgReceived = isempty(receivedMsg);
        %pause(0.5);
    end
    
    msg=strrep(receivedMsg,',',' ');
    msg=strrep(msg,'][',' ');
    msg=msg(2:end-1);

%     msg = insertAfter(receivedMsg,']',',')
%     msg = msg(1:end-1)
%     msg = ['[' msg ']']
    
    %Handle message string so that it becoms seperate rot och pos arrays
%     match = ["[","]"];
%     pose = split(receivedMsg, match);
%     pos = pose(2);
%     pos = split(pos,",");
    pos = str2num(msg);

    trans = pos(1:3);
    rot = pos(4:end);

%     while noMsgReceived
%         receivedMsg = char(read(t));
%         noMsgReceived = isempty(receivedMsg);
%         %pause(0.5);
%     end
%     match = ["[","]"];
%     pose = split(receivedMsg, match);
%     rot = pose(2);
%     rot = split(rot, ",");
%     rot = str2double(rot);

    %eulerRad = quat2eul(rot');
            %eulerDeg = rad2deg(eulerRad);
            %app.waitingOnPos = 0;
end

function packAndSendPose(~, pos, eulerDeg, t)
    %eulerRad = deg2rad(eulerDeg);
    %eulerDeg = [0,0,0];
    
    %rot = eul2quat(eulerRad)';
    
    %put together msg string
    sPos = string(pos);
    sRot = string(eulerDeg);
    
    
    %add formatting to pos string
    sPos = join(sPos,",");
    sPos = strcat("[",sPos,"]");
    
    %add formatting to rot string
    sRot = join(sRot,",");
    sRot = strcat("[",sRot,"]");

    pos = strcat ("[",sPos,",",sRot,"]");
    write(t,pos);

%     write(t,sPos);
%     write(t, sRot);
    
    %put pos and rot together
    %sendMsg = strcat(sPos,",",sRot);
    %sendMsg = strcat("[",sendMsg,"]");
    
    %send msg string
    %write(t,sendMsg)
end
>>>>>>> Stashed changes
