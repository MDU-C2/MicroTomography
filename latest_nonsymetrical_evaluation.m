close all
clear all
clc 
% Import DATA
% https://uwcem.ece.wisc.edu/phantomRepository.html
file_name = 'ClassIII_printed_phantom.stl';
geo = stlread (file_name);
raw_stl_points = geo.Points;


% Remove the plane and keep the breast 
breast_stl_points = raw_stl_points(raw_stl_points(:,3)>=6,:);



% Aproximate data center by looking att the plot
x_mid = 71;
y_mid = 65;
z_mid = 6;
% center the data
breast_stl_points(:,1) =breast_stl_points(:,1) -x_mid;
breast_stl_points(:,2) =breast_stl_points(:,2) -y_mid;
breast_stl_points(:,3) =breast_stl_points(:,3) -z_mid;



x = breast_stl_points(:,1);
y = breast_stl_points(:,2); 
z = breast_stl_points(:,3);

% figure; hold on; 
% scatter3(x,y,z)
% xlabel('X')
% ylabel('Y')
% zlabel('Z')
% title('Original')

[azimuth,elevation,r] = cart2sph(x,y,z);

r = r-3;

[scal_x,scal_y,scal_z] = sph2cart(azimuth,elevation,r);

shp = alphaShape(scal_x,scal_y,scal_z);

t_f = inShape(shp,x,y,z);
t_f = ~t_f;

% figure; hold on;
% scatter3(breast_stl_points(t_f,1),breast_stl_points(t_f,2),breast_stl_points(t_f,3))

x = breast_stl_points(t_f,1);
y = breast_stl_points(t_f,2); 
z = breast_stl_points(t_f,3);

[theta,rho,z] = cart2pol(x,y,z);

[z,sort_ind] = sort(z);
theta = theta(sort_ind);
rho = rho(sort_ind);

indx = find((rho<=36) & (z <3)); 
rho(indx) = [];
theta(indx) = [];
z(indx) = [];

[true_x,true_y,true_z] = pol2cart(theta,rho,z);

true_x = round(true_x*10)/10;
true_y = round(true_y*10)/10;
true_z = round(true_z*10)/10;

points = [true_x, true_y, true_z];
points = unique(points,'rows');

true_x = points(:,1);
true_y = points(:,2);
true_z = points(:,3);

figure; hold on;
scatter3(true_x,true_y,true_z)

% Consider true_x,true_y,true_z are the true values
clearvars -except true_x true_y true_z points
%% Try to sort the data in cartesian space
% 
% [theta,rho,pol_z] = cart2pol(true_x,true_y,true_z);
% 
% [theta,sort_ind] = sort(theta);
% pol_z = pol_z(sort_ind);
% rho = rho(sort_ind);
% 
% [x,y,z] = pol2cart(theta,rho,pol_z);
% 
% figure; hold on;
% for i = 1:length(x)
%     scatter3(x(i),y(i),z(i))
%     pause(0.00001)
% end
%% Spline resampling
% continue to sample from x, y, z 
[theta,rho,pol_z] = cart2pol(true_x,true_y,true_z);
% [theta,sort_ind] = sort(theta);
% pol_z = pol_z(sort_ind);
% rho = rho(sort_ind);
theta_deg = rad2deg(theta);

laser_angle = -180:18:180-18;
% theta_deg = round(theta_deg);
epsi = 2;
figure; hold on;
% scatter3(true_x,true_y,true_z,'.','blue')
for i = 1:size(laser_angle,2)
    sample_indx = find(( (theta_deg >(laser_angle(i)) ) &(theta_deg <=laser_angle(i) +epsi) )...
                        | ( (theta_deg <(laser_angle(i)) ) &(theta_deg >=laser_angle(i) -epsi) ));
    [samp_x,samp_y,samp_z] = pol2cart(theta(sample_indx),rho(sample_indx), pol_z(sample_indx));




    [spline_x,spline_y,spline_z] = pol2cart(deg2rad(laser_angle(i)),rho(sample_indx), pol_z(sample_indx));
    
    [spline_z,sort_ind] = sort(spline_z);
    spline_y = spline_y(sort_ind);
    spline_x = spline_x(sort_ind);
    
    [Cz, ai,ci] = unique(spline_z);
    Cx = spline_x(ai);
    Cy = spline_y(ai);



%     scatter3(samp_x,samp_y,samp_z)
%     scatter3(Cx,Cy,Cz,'filled')
    scatter3(0,0,max(true_z),'red','filled','o','LineWidth',50)
    
%   fix this
    n_points = 10;
    step_size = round(length(Cz)/(n_points));
    sampling_vec = step_size+1:step_size:length(Cx)-(step_size);
    sampling_vec = [1, sampling_vec, length(Cz)];

    scatter3(Cx(sampling_vec),Cy(sampling_vec),Cz(sampling_vec),'filled','red')
    
    display(length(sampling_vec))
end
