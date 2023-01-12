%Qucik Program to demo the use of findPointNormals
clc 
clear all
close all


new_code = load ('SurfacePoint11231426_NecCodeEm.mat');
new_code = new_code.surfacePoint;
points2 = new_code;
figure; hold on;
for i = 1:size(points2,3)
    [normals,curvature] = findPointNormals(points2(:,:,i),[],[0,0,10],true);

     
    scatter3(points2(:,1,i),points2(:,2,i),points2(:,3,i))
    quiver3(points2(:,1,i),points2(:,2,i),points2(:,3,i),...
    -normals(:,1),-normals(:,2),-normals(:,3),'r');

end
%%
% generate a set of 3d points
% x = repmat(1:49,49,1);
% y = x';
% z = peaks;
% points = [x(:),y(:),z(:)];

%find the normals and curvature
[normals,curvature] = findPointNormals(points,[],[0,0,10],true);

%plot normals and colour the surface by the curvature
hold off;
surf(x,y,z,reshape(curvature,49,49));
hold on;
quiver3(points(:,1),points(:,2),points(:,3),...
    -normals(:,1),-normals(:,2),-normals(:,3),'r');
axis equal;