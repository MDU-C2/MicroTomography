
posRobot=[10,0,10]
rot=[0,180,0]
laserlength=10;

position = findSurfacePosition(rot,posRobot,laserlength);

function position = findSurfacePosition(rot,posRobot,laserlength)
    d=[0,0,0]
    T1=createTransformationMatrix(rotx(rot(1)),posRobot)
    T2=createTransformationMatrix(roty(rot(2)),d)
    T3=createTransformationMatrix(rotz(rot(3)),d)

    laserlength=[0;0;laserlength;1];

    position = T1*T2*T3*laserlength;

    position=position(1:3)

end

function T=createTransformationMatrix(R,D)
    %Add new column
    D=rot90(D);
    T = [R D];
    T = [T ; [0,0,0,1]];
end