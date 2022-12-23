

% IF PLOT IS TRUE IT WILL TAKE TIME TO DRAW ALL THE POINTS, IF YOU DON't
% WANT TO WAIT SET PLOT TO 0. 
% PLOT IS USEFUL TO CHECK THE RESULT BEFORE SENDING THE COORDINATES TO YUMI

% function points = create_scan_points(boundary_height,hole_diameter,epsilon,z_step_size, azimuth_angle, laser_angle, plot)
points = create_scan_points(150,150,50,5, 18, 15, 0);
