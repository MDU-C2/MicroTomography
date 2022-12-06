clear all 
close all
clc

new_code = load ('SurfacePoint11231426_NecCodeEm.mat');
new_code = new_code.surfacePoint;
data = new_code;

%% ONE FUNCTION TO RUN ALL 
[test, test_normals, sim_data] = normal_scanning_protocol(data,30);

[geo,stl_points] = load_stl("symmetricalBreastModel.STL");

figure; hold on;
% trisurf(geo.ConnectivityList,stl_points(:,1),stl_points(:,2),stl_points(:,3))
xlabel('X Coordinates')
ylabel('Y Coordinates')
zlabel('Z Coordinates')

for i = 1:size(test,3)
    m = scatter3(sim_data(:,1,i),sim_data(:,2,i),sim_data(:,3,i),'filled','black');
    p = scatter3(test(:,1,i),test(:,2,i),test(:,3,i),'filled','red');
    ss = quiver3(test(:,1,i),test(:,2,i),test(:,3,i), ...
        test_normals(:,1,i),test_normals(:,2,i),test_normals(:,3,i));
end
legend([m,p,ss],'simulation data','Scan position','Z normal orientation')
%% Create simulated data

% simulate points from first spline 
azimuth = ((1:size(data,3))-1) .* 360/size(data,3) ;
spline = data (~isnan(data(:,1,1)),:,1); % clean from nan 
% Create array
sim_data = zeros(size(spline,1),3,size(data,3));
% Rotate spline 
for i = 1:size(azimuth,2)
    rotate = rotz(azimuth(i));
    rot_data = rotate*spline';
    sim_data(:,:,i) = rot_data';
end
%% Plot results 
figure; hold on;
for i = 1:size(sim_data,3)
    scatter3(sim_data(:,1,i),sim_data(:,2,i),sim_data(:,3,i),'filled','black')
    scatter3(data(:,1,i),data(:,2,i),data(:,3,i),'filled','red')
    view(3)
end

figure; hold on;
for i = 1:size(sim_data,3)
    scatter(sim_data(:,2,i),sim_data(:,3,i),'filled','black')
    scatter(data(:,2,i),data(:,3,i),'filled','red')
end

%%  Join spline
points = [];%zeros(size(power_crust_points,1)*size(power_crust_points,3),3);
for i = 1:size(sim_data,3)
    points = [points; sim_data(:,:,i)];
end

%% Create normals to surface 
[normals,curvature] = findPointNormals(points,[],[0,0,10],true);
% Normals are unit length
%% Show normals 
fig = figure; 
ax = axes; 
hold(ax,'on'); 
scatter3(points(:,1),points(:,2),points(:,3))
quiver3(points(:,1),points(:,2),points(:,3),...
-normals(:,1),-normals(:,2),-normals(:,3),'r');
% scatter3(points(1,1),points(1,2),points(1,3),'filled','black')

% scatter3(scan_point(1),scan_point(2),scan_point(3),'filled','blue')

% quiver3(points(1,1),points(1,2),points(1,3),axis(1),axis(2),axis(3),20,'black')
 show_HT(fig,ax,HT,30)
%% Reshape data to spline
scan_points = zeros(size(sim_data));
scan_normals = zeros(size(sim_data));
for i = 1:size(sim_data,3)
    indexes = ((size(sim_data,1)*(i-1))+1):(size(sim_data,1)*i);
    scan_points(:,:,i) = points(indexes,:);
    scan_normals(:,:,i) = normals(indexes,:);
end

%% Find Rotation matrix that maps Z to normal 
distance = 30;

for i = 1:size(scan_points,1)
    for j = 1:size(scan_points,3)
        % Calculate Z X normals = get axis rotation 
        axis = cross([0,0,1],-scan_normals(i,:,j));
        % Calculate angle between Z and X but dot product 
        angle = acos(dot([0,0,1],-scan_normals(i,:,j)));
        % Create rotation matrix from axis angle above 
        rot = axang2rotm([axis, angle]);
        % Find the point at a certain distance 
    
        scan_point = scan_points(i,:,j) + distance*-scan_normals(i,:,j);
        % Create HT 
        HT = se3(rot,scan_point);
        % Show HT 
        laser_posistions(i,:,j) = [HT.trvec rad2deg(tform2eul(HT.tform))];  
        %show_HT(fig,ax,HT,30)
    end
end

%%
[geo,stl_points] = load_stl("symmetricalBreastModel.STL");

figure(fig); hold on;
trisurf(geo.ConnectivityList,stl_points(:,1),stl_points(:,2),stl_points(:,3))
xlabel('X Coordinates')
ylabel('Y Coordinates')
zlabel('Z Coordinates')
scatter3(stl_points(:,1),stl_points(:,2),stl_points(:,3),'filled','red')

%%
figure; hold on;
for i = 1:size(laser_posistions,3)
    scatter3(laser_posistions(:,1,i),laser_posistions(:,2,i),laser_posistions(:,3,i))
    quiver3(laser_posistions(:,1,i),laser_posistions(:,2,i),laser_posistions(:,3,i),scan_normals(:,1,i),scan_normals(:,2,i),scan_normals(:,3,i))
end
