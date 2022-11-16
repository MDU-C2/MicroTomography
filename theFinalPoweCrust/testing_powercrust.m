%% Generate simulated data 
clear all  
close all  
clc 
azimuth_angle= 7 
boundary_height = 200; 
% Heights for scanning points  
z_step_size = 20; % Height slice step size 
num_z_step = (boundary_height)/(z_step_size); % number of steps  
% Z of all scanning heights 
Z = linspace(-z_step_size,-boundary_height, num_z_step); 
% Make it better later 
 
azimuth = (pi.*linspace(0,360-azimuth_angle,360/azimuth_angle))./180 ; 
 
 
points = zeros(num_z_step,3,length(azimuth)); 
 
 
for i = 1:length(azimuth) 
    for j = 1:length(Z) 
        Radius = sqrt( (Z(j)+200)/0.02 );  
        % Create coordinate in base space 
        points(j,1,i) = Radius.*cos(azimuth(i)); 
        points(j,2,i) = Radius.*sin(azimuth(i)); 
        points(j,3,i) = Z(j); 
 
    end 
end 
 
 
 
figure;hold on; 
for i = 1:length(azimuth) 
    scatter3(points(:,1,i),points(:,2,i),points(:,3,i)) 
end 
%% try cylinder
clear all  
close all  
clc 
azimuth_angle= 3 
boundary_height = 200; 
% Heights for scanning points  
z_step_size = 1; % Height slice step size 
num_z_step = (boundary_height)/(z_step_size); % number of steps  
% Z of all scanning heights 
Z = linspace(-z_step_size,-boundary_height, num_z_step); 
% Make it better later 
 
azimuth = (pi.*linspace(0,360-azimuth_angle,360/azimuth_angle))./180 ; 
 
 
points = zeros(num_z_step,3,length(azimuth)); 
 
Radius = 200/2;  
for i = 1:length(azimuth) 
    for j = 1:length(Z) 

        % Create coordinate in base space 
        points(j,1,i) = Radius.*cos(azimuth(i)); 
        points(j,2,i) = Radius.*sin(azimuth(i)); 
        points(j,3,i) = Z(j); 
 
    end 
end 
 
 
 
figure;hold on; 
for i = 1:length(azimuth) 
    scatter3(points(:,1,i),points(:,2,i),points(:,3,i)) 
end 

 
%% 
point_list = []; 
for i = 1:size(points, 3) 
    point_list = [point_list; points(:,:,i)]; 
end 
figure;  
scatter3(point_list(:,1),point_list(:,2),point_list(:,3)) 
tic
[~,Mesh,~,~,~] = PowerCrust(point_list,1); 
toc