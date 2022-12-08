clear all 
close all
clc


new_code0 = load ('surfacePoint12081126_90deg_5step_0degsurf.mat');
new_code0 = new_code0.surfacePoint;
data0 = new_code0;

% Inputs
num_splines = 20;
data = data0(:,:,4);
data(:,3) = data(:,3)-25.5096
distance = 50;

% simulate points from first spline 
azimuth = linspace(0,360-(360/num_splines),num_splines) ;
spline = data (~isnan(data(:,1)),:); % clean from nan 
% Create array
sim_data = zeros(size(spline,1),3,num_splines);
% Rotate spline 
for i = 1:size(azimuth,2)
    rotate = rotz(azimuth(i));
    rot_data = rotate*spline';
    sim_data(:,:,i) = rot_data';
end

%%  Join spline
points = [];%zeros(size(power_crust_points,1)*size(power_crust_points,3),3);
for i = 1:num_splines
    points = [points; sim_data(:,:,i)];
end

%% Create normals to surface 
[normals,curvature] = findPointNormals(points,[],[0,0,10],true);
% Normals are unit length
%% Reshape data to spline
scan_points = zeros(size(sim_data));
scan_normals = zeros(size(sim_data));
for i = 1:size(sim_data,3)
    indexes = ((size(sim_data,1)*(i-1))+1):(size(sim_data,1)*i);
    scan_points(:,:,i) = points(indexes,:);
    scan_normals(:,:,i) = normals(indexes,:);
end
%% Find Rotation matrix that maps Z to normal 
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
selected = [1,6,11,16];
scan_protocol = laser_posistions(:,:,selected);
selected_sim_data = sim_data(:,:,selected);
selected_normals = scan_normals(:,:,selected);
scan_protocol (end,:,:) = [];
selected_normals (end,:,:) = [];


figure; hold on; 
[geo,stl_points] = load_stl("symmetricalBreastModel.STL");

fig = figure; hold on;
% trisurf(geo.ConnectivityList,stl_points(:,1),stl_points(:,2),stl_points(:,3))
xlabel('X Coordinates')
ylabel('Y Coordinates')
zlabel('Z Coordinates')
scatter3(stl_points(:,1),stl_points(:,2),stl_points(:,3),'red')

%
figure(fig); hold on;
for i = 1:size(scan_protocol,3)
    scatter3(selected_sim_data(:,1,i),selected_sim_data(:,2,i),selected_sim_data(:,3,i),'filled')
    scatter3(scan_protocol(:,1,i),scan_protocol(:,2,i),scan_protocol(:,3,i))
    quiver3(scan_protocol(:,1,i),scan_protocol(:,2,i),scan_protocol(:,3,i),selected_normals(:,1,i),selected_normals(:,2,i),selected_normals(:,3,i))
end
%% 
selected = [1,16,31,46];
scan_protocol = laser_posistions(:,:,selected);
