clc
clear
close all;

laserlength=10;

t = tcpclient('192.168.125.1',55000);

while true
    [pos, rot] = ReceiveAndUnpackPose(0, t);
    %posRobot=[-100,0,0];
    %rot=[0,90,0];
    scatter3(pos(1),pos(2),pos(3),'filled');
    position = findSurfacePosition(rot,pos,laserlength);
    scatter3(position(1),position(2),position(3));
    pause(.1);
    hold on;
end


function position = findSurfacePosition(rot,posRobot,laserlength)
    d=[0;0;0];
    laserlength=[0;0;laserlength;1];

    T1=createTransformationMatrix(rotz(rot(3)),posRobot);
    T2=createTransformationMatrix(roty(rot(2)),d);
    T3=createTransformationMatrix(rotx(rot(1)),d);
    T = T1*T2*T3;

    position = T*laserlength;
    position=position(1:3)
end

function T=createTransformationMatrix(R,D)
    %disp(D)
    %D=D';
    %disp(D)
    T = [R D];
    T = [T ; [0,0,0,1]];
end

function [pos, rot] = ReceiveAndUnpackPose(~, t)
            %app.waitingOnPos = 1;
            %wait until message is received
            noMsgReceived = 1;
            while noMsgReceived
                receivedMsg = char(read(t));
                noMsgReceived = isempty(receivedMsg);
                %pause(0.5);
            end
            %Handle message string so that it becoms seperate rot och pos arrays
            match = ["[","]"];
            pose = split(receivedMsg, match);
            pos = pose(2);
            pos = split(pos,",");
            pos = str2double(pos);

            while noMsgReceived
                receivedMsg = char(read(t));
                noMsgReceived = isempty(receivedMsg);
                %pause(0.5);
            end
            match = ["[","]"];
            pose = split(receivedMsg, match);
            rot = pose(2);
            rot = split(rot, ",");
            rot = str2double(rot);

            %eulerRad = quat2eul(rot');
            %eulerDeg = rad2deg(eulerRad);
            %app.waitingOnPos = 0;
end