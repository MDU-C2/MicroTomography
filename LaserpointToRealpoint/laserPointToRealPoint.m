clc
clear
close all;

laserlength=10;
posRobot=[-100,0,0];
rot=[0,90,0];

position = findSurfacePosition(rot,posRobot,laserlength);

function position = findSurfacePosition(rot,posRobot,laserlength)
    d=[0,0,0];
    laserlength=[0;0;laserlength;1];

    T1=createTransformationMatrix(rotz(rot(3)),posRobot);
    T2=createTransformationMatrix(roty(rot(2)),d);
    T3=createTransformationMatrix(rotx(rot(1)),d);
    T = T1*T2*T3;

    position = T*laserlength;
    position=position(1:3)
end

function T=createTransformationMatrix(R,D)
    D=D';
    T = [R D];
    T = [T ; [0,0,0,1]];
end