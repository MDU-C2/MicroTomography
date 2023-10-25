 
function surfacePoints = calcSurfacePoint(LaserPoints)
   surfacePoints=zeros( size(LaserPoints,1), 3, size(LaserPoints,3));
   for s = 1:size(LaserPoints,3)
        for r = 1:size(LaserPoints,1)
            %Take next elements in array TRANS ROT
            if ~isnan(LaserPoints(r,1,s))
                surfacePoint = findSurfacePosition(LaserPoints(r,1:3,s), LaserPoints(r,4:6,s), LaserPoints(r,7,s));
                surfacePoints(r,:,s) = surfacePoint;
            else
                surfacePoints(r,:,s) = [NaN,NaN,NaN];
            end

            scatter3(LaserPoints(r,1,s),LaserPoints(r,2,s),LaserPoints(r,3,s),'filled')
            hold on;
            scatter3(surfacePoints(r,1,s),surfacePoints(r,2,s),surfacePoints(r,3,s));
            hold on;
        end
   end
end

%             scatter3(pos(1),pos(2),pos(3),'filled');
%             hold on;
%             laserlength=20;
%             position = findSurfacePosition(obj, rot,pos,laserlength);
%             scatter3(position(1),position(2),position(3));
%             pause(.1);
%             hold on;
