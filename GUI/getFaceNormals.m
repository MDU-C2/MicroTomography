function [centerPoints, normals] = getFaceNormals(app, shp)
%get triangle connectivity
[tri, xyz] = boundaryFacets(shp);
%split columns into points
p1 = tri(:, 1);
p2 = tri(:, 2);
p3 = tri(:, 3);
%go through each triangle and get the normals
for i = 1:length(tri)
    trianglePoints(1, :) = xyz(p1(i), :);
    trianglePoints(2, :) = xyz(p2(i), :);
    trianglePoints(3, :) = xyz(p3(i), :);
    centerPoints(i, :) = mean(trianglePoints); %get triangle center point
    normal(i, :) = cross(trianglePoints(1,:)-trianglePoints(2,:), trianglePoints(1,:)-trianglePoints(3, :));
    normals(i, :) = -(normal(i, :) / norm( normal(i, :) )); % just to make it unit length
end
end