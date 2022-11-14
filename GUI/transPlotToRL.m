function newP = transPlotToRL(app, pX, pY, pZ, diffRLplot)
%translates plot's coordinate system to the robot coordinate
%system by subtracting the saved difference from translating to plot coordinates.
newP(:, 1) = pX - diffRLPlot(1);
newP(:, 2) = pY - diffRLPlot(2);
newP(:, 3) = pZ - diffRLPlot(3);
end