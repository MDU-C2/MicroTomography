function newP = transPlotToRL(app, pX, pY, pZ, diffRLplot)
%translates plot's coordinate system to the robot coordinate
%system by subtracting the saved difference from translating to plot coordinates.
newP(:, 1) = pX - diffRLplot(1);
newP(:, 2) = pY - diffRLplot(2);
newP(:, 3) = pZ - diffRLplot(3);
end