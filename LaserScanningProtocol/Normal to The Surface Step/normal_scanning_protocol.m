function [laser_posistions, scan_normals, sim_data] = normal_scanning_protocol(data,num_splines, distance)
%% Create simulated data from first spline
% Rotate the first spline of the data into different azimuth angles. 
% this creates simulated data , because the algorithm may have difficulties
% with the current unbalanced data because of yumi calibration 

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
end

