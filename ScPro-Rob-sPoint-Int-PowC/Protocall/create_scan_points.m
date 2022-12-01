function points = create_scan_points(boundary_height,hole_diameter,epsilon,z_step_size, azimuth_angle, laser_angle, plot)
% Create yumi cylindrical scanning positions.
%=========================================================================%
% Output 
% Points 6 Dimensional array  
    % Positon ( X, Y, Z) in the base coordinate. 
    % Orientation (eul_Z, eul_Y, eul_X) in the base coordinate orientation.
%=========================================================================%
% Base coordinate system 
    % Base coordinate is in the center of the hole with Z pointing up. 
    % X points away from the hole center. 
%=========================================================================%
% Input
    % boundary_height: Max height of the scanning cylinder. 
    % Hole_diameter: Diameter of the hole. 
    % % epsilon: Extra margin from the hole diamter. 
    % z_step_size: Step size between scanning points in Z direction. 
    % azimuth_angle:(degrees) The difference between scanning angles, given
    % in degrees
    % Laser angle: The angle of the laser with Z axis in degree
% number of steps in Z direction 
num_z_step = (boundary_height)/(z_step_size); 
% Create all Z coordinates for all Z 
Z = linspace(0,-boundary_height, num_z_step+1);
% Create the azimuth angle of all coordinates. 
azimuth = (pi.*linspace(0,360-azimuth_angle,360/azimuth_angle))./180 ;
% Radius of the hole + an extra margin
R_epsi = hole_diameter/2 + epsilon;
% Points declaration 
points = zeros(length(Z),6,length(azimuth));

if plot  == true
    fig = figure;
    axis = axes;
    hold(axis, "on")
end

for i = 1:length(azimuth)
    for j = 1:length(Z)
        % Create (X, Y, Z) coordinate in base space
        point_c_space(:,1) = R_epsi.*cos(azimuth(i));
        point_c_space(:,2) = R_epsi.*sin(azimuth(i));
        point_c_space(:,3) = Z(j);
        % Create Homogeneous Transformations with orientation
        HT = se3(rotz(180)*roty(90+laser_angle)*rotx(rad2deg(-azimuth(i))),point_c_space);

        if plot == true 
            show_HT(fig,axis, HT,20 )
        end
        % Create points by extracting euler 
        points(j,:,i) = [HT.trvec rad2deg(tform2eul(HT.tform))];        
    end
end
end

