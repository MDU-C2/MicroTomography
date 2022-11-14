function  [newP, diffRLPlot] = transRLtoPlot(app, P, diffRLPlot)
%translates the robot coordinate system to plot coordinate
%system, so that the model's center always is in origo (0,0,0)
t = exist('diffRLPlot','var');
if exist('diffRLPlot','var') == 0 || isempty(diffRLPlot)
    centerX = mean(P(:, 1));
    centerY = mean(P(:, 2));
    centerZ = mean(P(:, 3));

    diffRLPlot = zeros(3, 1);
    diffRLPlot(1) = -centerX;
    diffRLPlot(2) = -centerY;
    diffRLPlot(3) = -centerZ;

end

newP(:, 1) = P(:,1) + diffRLPlot(1);
newP(:, 2) = P(:,2) + diffRLPlot(2);
newP(:, 3) = P(:,3) + diffRLPlot(3);

end