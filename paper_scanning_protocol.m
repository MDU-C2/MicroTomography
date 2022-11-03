% This is a scanning protocol as mentioned in the journal 
% "Surface Estimation for Microwave Imaging"
% Link to the journal : 
% https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5539471/
%=========================================================================%

% The algoritm should know the coordinate of the center of the hole in the 
% table and The diameter of the whole. 

% The function work in the coordinate system that have the hole center as
% origo and 

hole_diameter = 200 ; %CM 
epsilon = 100;
% it assumes a cylindrical boundary box arround the table hole. 
% The cylindrical boundary center matches the hole in the table and have
% the same diameter. 
% The maximum heigh is assumed to be 20 cm 
boundary_height = 200;



% Heights for scanning points 

z_step_size = 5; % Height slice step size

num_z_step = (boundary_height)/(z_step_size); % number of steps 

% Z of all scanning heights
Z = linspace(0,-boundary_height, num_z_step+1);

% Make it better later
azimuth = (pi.*linspace(0,360-18,21))./180 ;

R_epsi = hole_diameter/2 + epsilon;

scan_points = [];
fig = figure; 
axis = axes;
hold(axis, "on")

for i = 1:length(azimuth)
 
    for j = 1:length(Z)
        % Create coordinate in base space
        point_c_space(:,1) = R_epsi.*cos(azimuth(i));
        point_c_space(:,2) = R_epsi.*sin(azimuth(i));
        point_c_space(:,3) = Z(j);

        % Create Homogeneous Transformations with orientation
        HT = se3(roty(90)*rotx(rad2deg(-azimuth(i))),point_c_space);

        %show_HT(fig, axis,HT,10)

        % Convert to position and roll pith yaw
        scan_pos = [HT.trvec, tform2eul(HT.tform)];
        
        scan_points = [scan_points;scan_pos];
    end

end
%%
scan_points = create_scan_points(200,200,100,5);
%% Open connection 
tcp_con = tcpclient('192.168.125.1',55000);

if tc_con == "open"

else 
    display(" TCP Connection failed")
end




%% Scanning protocol 

% For all points in protocol 
    % Create point                              ===Done
    % Send it to Yumi                           ===Done
    % Read from Yumi                            === Done
    % Read from sensor                          === Done
    % Convert yumi pos and sensor value to (x,y,z) in cartezian space == ? 

% interpolate points to get splines             == ToDo Victor
% Find intersection between splines and planes  == ToDo Victor
% Interpolate intersection points to eclipse    == ToDo Victor
% Uniformaly resample the shape                 == ToDo Victor
% Crust Algorithm                               == Todo Jonathan 
% Return Surface 

%%
hole_diameter = 200 ; %CM 
epsilon = 100;
% it assumes a cylindrical boundary box arround the table hole. 
% The cylindrical boundary center matches the hole in the table and have
% the same diameter. 
% The maximum heigh is assumed to be 20 cm 
boundary_height = 200;
R_epsi = hole_diameter/2 + epsilon;


% Heights for scanning points 

z_step_size = 5; % Height slice step size

num_z_step = (boundary_height)/(z_step_size); % number of steps 
% Z of all scanning heights
Z = linspace(0,-boundary_height, num_z_step+1);

point_c_space(:,1) = R_epsi.*cos(0);
point_c_space(:,2) = R_epsi.*sin(0);
point_c_space(:,3) = Z(1);

        % Create Homogeneous Transformations with orientation
HT = se3(roty(-90)*rotx(0),point_c_space)

new_z = HT.transform([0,0,1])
new_z = HT.trvec -new_z
 translation_vec = HT.trvec;
        

figure;
quiver3( translation_vec(1),translation_vec(2),translation_vec(3),...
            new_z(1),new_z(2),new_z(3))

%%
epsilon = 100;
z_step_size = 5;
points = create_scan_points(epsilon,z_step_size);

%%

figure;
hold on;
% Plot points 
for point_idx = 1:length(scan_points)
    scatter3(scan_points(point_idx,1),scan_points(point_idx,2),scan_points(point_idx,3))
end

