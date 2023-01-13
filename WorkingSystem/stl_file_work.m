geo = stlread ("V2_realaaaa.STL")
new_points = rotx(90)*geo.Points';
new_points = new_points';

figure; 
trisurf(geo.ConnectivityList,new_points(:,1),new_points(:,2),new_points(:,3))
xlabel('X Coordinates')
ylabel('Y Coordinates')
zlabel('Z Coordinates')


% direction = [1 0 0];
% rotate(geo,direction,90)
