clc
clear
close all;

laserlength=10;

posRobot=[-100,0,0];
rot=[0,90,0];
position = findSurfacePosition(rot,posRobot,laserlength,'r');

posRobot=[0,100,0];
rot=[-46.66,90,-136.677];
position = findSurfacePosition(rot,posRobot,laserlength,'g');

posRobot=[100,0,0];
rot=[51.743,90,-128.57];
position = findSurfacePosition(rot,posRobot,laserlength,'b');

posRobot=[0,-100,0];
rot=[-25.154,90,65];
position = findSurfacePosition(rot,posRobot,laserlength,'m');

posRobot=[100,0,0];
rot=[-47.24,90,132.75];
position = findSurfacePosition(rot,posRobot,laserlength,'k');

function position = findSurfacePosition(rot,posRobot,laserlength,f)
    d=[0,0,0];
    laserlength=[0;0;laserlength;1];

    T1=createTransformationMatrix(rotz(rot(3)),posRobot);
    T2=createTransformationMatrix(roty(rot(2)),d);
    T3=createTransformationMatrix(rotx(rot(1)),d);

    
    T = T1*T2*T3;

    position = T*laserlength;

    position=position(1:3)
    scatter3(posRobot(1),posRobot(2),posRobot(3),'*',f)
    hold on;
    scatter3(position(1),position(2),position(3),'filled',f)
    hold on;
end

function T=createTransformationMatrix(R,D)
    %Add new column
    D=D';
    T = [R D];
    T = [T ; [0,0,0,1]];
end