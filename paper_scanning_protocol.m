% This is a scanning protocol as mentioned in the journal 
% "Surface Estimation for Microwave Imaging"
% Link to the journal : 
% https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5539471/
%=========================================================================%

% The algoritm should know the coordinate of the center of the hole in the 
% table and The diameter of the whole. 

% Example of a hole center coordinate in Yumi space 
hole_center = [10, 20, 40];
hole_diameter = 20 ; %CM 

% it assumes a cylindrical boundary box arround the table hole. 
% The cylindrical boundary center matches the hole in the table and have
% the same diameter. 
% The maximum heigh is assumed to be 20 cm 
boundary_height = 20;



% Heights for scanning points 

z_step_size = 0.5; % Height slice step size
num_z_step = (hole_center(3)-boundary_height)/(0.5); % number of steps 
% Z of all scanning heights
Z = linspace(hole_center(3),(hole_center(3)-boundary_height), num_z_step+1);


azimuth = (pi.*linspace(0,360,21))./180 ;

r = hole_diameter/2;

scan_points = [];

for i = 1:length(azimuth)
 
    for j = 1 :length(Z)
        point(:,1) = r.*cos(azimuth(i));
        point(:,2) = r.*sin(azimuth(i));
        point(:,3) = Z(j);
        scan_points = [scan_points;point];
    end

end
% Remove the last scan as 2pi and 0 are the same azimuth 
%.......

figure;
hold on;
% Plot points 
for point_idx = 1:length(scan_points)
    scatter3(scan_points(point_idx,1),scan_points(point_idx,2),scan_points(point_idx,3))
    drawnow
end

