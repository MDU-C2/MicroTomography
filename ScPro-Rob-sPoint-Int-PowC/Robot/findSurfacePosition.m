function position = findSurfacePosition(posRobot,rot,laserlength)
    d=[0,0,0];
    laserlength=[0;0;laserlength;1];

    T1=createTransformationMatrix(rotx(rot(3)),posRobot);
    T2=createTransformationMatrix(roty(rot(2)),d);
    T3=createTransformationMatrix(rotx(rot(1)),d);
    T = T1*T2*T3;

    position = T*laserlength;
    position=position(1:3)';

end