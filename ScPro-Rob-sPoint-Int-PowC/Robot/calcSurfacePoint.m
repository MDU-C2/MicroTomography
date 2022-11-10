 
function surfacePoints = calcSurfacePoint(LaserPoints)
   surfacePoints=zeros( size(LaserPoints,1), 3, size(LaserPoints,3));
   for s = 1:size(LaserPoints,3)
        for r = 1:size(LaserPoints,1)
            %Take next elements in array TRANS ROT
            surfacePoint = findSurfacePosition(LaserPoints(r,1:3,s), LaserPoints(r,4:6,s), LaserPoints(r,7,s));
            surfacePoints(r,:,s) = surfacePoint;
        end
   end
end
