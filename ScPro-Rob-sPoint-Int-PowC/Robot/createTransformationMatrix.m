function T=createTransformationMatrix(R,D)
    D=D';

    T = [R D];
    T = [T ; [0,0,0,1]];
end        