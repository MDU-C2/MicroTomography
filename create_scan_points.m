function scan_points = create_scan_points(epsilon,z_step_size)
%CREATE_SCAN_POINTS Summary of this function goes here
%   Detailed explanation goes here

hole_diameter = 200 ; %CM 

% it assumes a cylindrical boundary box arround the table hole. 
% The cylindrical boundary center matches the hole in the table and have
% the same diameter. 
% The maximum heigh is assumed to be 20 cm 
boundary_height = 200;


num_z_step = (boundary_height)/(z_step_size); % number of steps 

% Z of all scanning heights
Z = linspace(0,-boundary_height, num_z_step+1);

% Make it better later
azimuth = (pi.*linspace(0,360-18,21))./180 ;

R_epsi = hole_diameter/2 + epsilon;

scan_points = [];

for i = 1:length(azimuth)
 
    for j = 1 :length(Z)
        % Create coordinate in base space
        point_c_space(:,1) = R_epsi.*cos(azimuth(i));
        point_c_space(:,2) = R_epsi.*sin(azimuth(i));
        point_c_space(:,3) = Z(j);

        % Create Homogeneous Transformations with orientation
        HT = se3(roty(90)*rotx(azimuth(i)),point_c_space);
        
        % Convert to position and roll pith yaw
        scan_pos = [HT.trvec, tform2eul(HT.tform)];

        scan_points = [scan_points;scan_pos];
    end

end


end

