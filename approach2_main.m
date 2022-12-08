clear all 
close all
clc

new_code = load ('surfacePoint12081116_90deg_10step_ExtraAngleBeginning_calb.mat');
new_code = new_code.surfacePoint;
data = new_code;

new_code0 = load ('surfacePoint12081126_90deg_5step_0degsurf.mat');
new_code0 = new_code0.surfacePoint;
data0 = new_code0;

[geo,stl_points] = load_stl("symmetricalBreastModel.STL");
fig = figure; hold on ; 
for i = 4
    scatter3(data(:,1,i),data(:,2,i),data(:,3,i)-25.5096,'red')
    scatter3(data0(:,1,i),data0(:,2,i),data0(:,3,i)-25.5096,'filled','black')
end
figure(fig); hold on; 
scatter3(stl_points(:,1),stl_points(:,2),stl_points(:,3),'magenta')
xlabel('X')

rotate = rotz(3.5);
rot_stl = rotate*stl_points';
rot_stl = rot_stl';

% extract spline points 
true_spline = rot_stl((round(rot_stl(:,1)) == 0) & rot_stl(:,2)<=0 ,:);
figure(fig); hold on; 
scatter3(true_spline(:,1),true_spline(:,2),true_spline(:,3),'filled','blue')

true_spline(1,:) = [];
[~, indx] = sort(true_spline(:,3),1);
true_spline = true_spline(indx,:);
%% plot 2 dimensions 
figure; hold on; 
scatter3(true_spline(:,1),true_spline(:,2),true_spline(:,3),'blue')
scatter3(data(:,1,4),data(:,2,4),data(:,3,4)-25.5096,'red')
scatter3(data0(:,1,4),data0(:,2,4),data0(:,3,4)-25.5096,'black')
%% ONE FUNCTION TO RUN ALL 
[test, test_normals, sim_data] = normal_scanning_protocol(data(:,:,4),20,30);

[geo,stl_points] = load_stl("symmetricalBreastModel.STL");

figure; hold on;
trisurf(geo.ConnectivityList,stl_points(:,1),stl_points(:,2),stl_points(:,3))
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
%% Create simulated data klad
delta_z = 5;
num_z = 50;
scan_data = data(:,:,[1,6,11,16]);
azimuth = linspace(0,360-(360/size(scan_data,3)),size(scan_data,3));

resample_spline = zeros(num_z,3,size(scan_data,3));

for i = 1:size(scan_data,3)
    spline = scan_data (~isnan(scan_data(:,1,i)),:,i); % clean from nan
    x = spline(:,1);
    y = spline(:,2);
    z = spline(:,3);

    if i == 1 || i == 11
    x_spline = smooth_spline_zx(z,x,false);
    y_spline = poly2_fit(z,y,false);
    elseif i == 6 || i == 16
        x_spline = poly2_fit(z,x,false);
        y_spline = smooth_spline_zx(z,y,false);
    end
    new_z = linspace(max(z),min(z), num_z);
%     resampled_spline = 
    

end
%% Create simulated data klad
scan_data = data(:,:,[1,6,11,16]);
azimuth = linspace(0,360-(360/size(scan_data,3)),size(scan_data,3));

[~,idx] = max(sum(isnan(scan_data(:,1,:))));
shortest_spline = data (~isnan(data(:,1,idx)),:,idx); % clean from nan 
data_length = size(shortest_spline(:,3,idx),1);
for i = 1:size(scan_data,3)
    spline = data (~isnan(data(:,1,i)),:,i); % clean from nan
    spline = spline(1:data_length,:); % cut to max length
    x = spline(:,1);
    y = spline(:,2);
    z = spline(:,3);

    if i == 1 || i == 11
    x_spline = smooth_spline_zx(z,x,false);
    y_spline = poly2_fit(z,y,false);
    elseif i == 6 || i == 16
        x_spline = poly2_fit(z,x,false);
        y_spline = smooth_spline_zx(z,y,false);
    end
end



%% Create simulated data
zmin = min(min(data(:,3,:)));
step_size = 2;
new_z = -1*(0:step_size:abs(zmin)); % contunie here
% simulate points from first spline 
azimuth = ((1:size(data,3))-1) .* 360/size(data,3) ;

num_spline_needed= 20;

resampled_spline = zeros(size(new_z,2),3,num_spline_needed);
rotation_angles = linspace(0,90,(num_spline_needed/4)+1);%size(data,3);
%rotation_angles([1,end]) = [];

for i = [1,6,11,16]
    spline = data (~isnan(data(:,1,i)),:,i); % clean from nan 
    x = spline(:,1);
    y = spline(:,2);
    z = spline(:,3);
    if i == 1 || i == 11
        x_spline = smooth_spline_zx(z,x,false);
        y_spline = poly2_fit(z,y,false);
    elseif i == 6 || i == 16
        x_spline = poly2_fit(z,x,false);
        y_spline = smooth_spline_zx(z,y,false);
    end
    rot_data = zeros(size(new_z,2),3,num_spline_needed);
    for j = 1:size(rotation_angles,2)
        
        rot_data(:,1,i+j) = x_spline(new_z);
        rot_data(:,2,i+j) = y_spline(new_z);
        rot_data(:,3,i+j) = new_z;
        rotate = rotz(rotation_angles(j));

        resampled_spline(:,:,i+j) = transpose(rotate*rot_data(:,:,i+j)');

    end
    
end

%% Plot results 

figure; hold on;
for j = [1,6,11,16]
    scatter3(resampled_spline(:,1,j),resampled_spline(:,2,j),resampled_spline(:,3,j),'filled','black')
    view(3)
end
hold on;
for i = 1:size(resampled_spline,3)
    scatter3(data(:,1,i),data(:,2,i),data(:,3,i),'filled','red')
    view(3)
end

figure; hold on;
for i = 1:size(resampled_spline,3)
    scatter(resampled_spline(:,2,i),resampled_spline(:,3,i),'filled','black')
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
