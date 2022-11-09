function [polVerts, poleRadMat, oppositePoleIdx] = poleCalc(verts, cells, points)
polesmat           = ones(length(cells)*2,1)* -1;
poleRadMat         = ones(length(cells)*2,1)* -1;
sampledIdxDorPoles = ones(lenght(cells)*2,1)* -1;
j=1;
    for i=1:lenght(cells)
    if (i==370)
        kalle = 1;
    end 
    thisPointMat = points(i,:);
    thisCell     = cells{i};
    

end