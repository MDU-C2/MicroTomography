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

points = zeros(length(Z),6,length(azimuth));

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

        points(j,:,i) = [HT.trvec tform2eul(HT.tform)];
        
    end

end
%%
scan_points = create_scan_points(200,200,100,5,7);
figure;hold on;
for i = 1:size(scan_points,3)
    scatter3(scan_points(:,1,i),scan_points(:,2,i),scan_points(:,3,i))
    view(3)
    drawnow
end

%% Open connection 
tcp_con = tcpclient('192.168.125.1',55000);
%..... From GUI Functions


%% Generate simulated data
clear all 
close all 
clc
azimuth_angle = 7
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

%% Interpolate spline from data 
boundary_height = 200;
% Heights for scanning points 
z_step_size = 5; % Height slice step size,

azimuth = (pi.*linspace(0,360-18,21))./180 ;
num_z_step = (boundary_height)/(z_step_size); % number of steps 
zz =  linspace(-z_step_size,-boundary_height, num_z_step);

ppoints = zeros(length(zz),3,length (azimuth));
linspace(-z_step_size,-boundary_height, num_z_step);
for i = 1:length(azimuth)
    ppx(:,i) = spline (points(:,3,i),points(:,1,i));
    ppy(:,i) = spline (points(:,3,i),points(:,2,i));

    
    ppoints(:,1,i) = ppval(ppx(:,i),zz);
    ppoints(:,2,i) = ppval(ppy(:,i),zz);
    ppoints(:,3,i) = zz;
  
end
    figure;hold on;
for i = 1:length(azimuth)
    
    scatter3(points(:,1,i),points(:,2,i),points(:,3,i),'filled')
    plot3(ppoints(:,1,i),ppoints(:,2,i),ppoints(:,3,i))
    scatter3(ppoints(:,1,i),ppoints(:,2,i),ppoints(:,3,i),'red')
    

end
legend('Scanning Points', 'Aproximated function', 'Uniformly resampled')
%% Function 
boundary_height = 200;
ppoints = resampling(points,5,boundary_height);

figure;
scatter3(ppoints(:,1),ppoints(:,2),ppoints(:,3))

%% extract spline intersection with Z
for z = -160
    for i = 1:length(ppx)
        circle_points_x(i) = ppval(ppx(1,i),z);
        circle_points_y(i) = ppval(ppy(1,i),z);
    end
end
    figure;hold on;
for i = 1:length(azimuth)
    
    scatter3(circle_points_x(:),circle_points_y(:),z,'filled')
    plot3(ppoints(:,1,i),ppoints(:,2,i),ppoints(:,3,i))
    
end
legend('Scanning Points', 'Aproximated function')

figure; 
scatter(circle_points_x(:),circle_points_y(:))



%% interpolate in a ellipse 
% Test using 
% https://se.mathworks.com/help/matlab/math/example-curve-fitting-via-optimization.html
% Otherwise follow paper 
xxx=circle_points_x;
yyy=circle_points_y;
scatter(xxx,yyy);
axis([-50 50 -50 50]);
axis equal;
initialparameter=[10 10 0];
mx=@(initialparameter)error_function(initialparameter,xxx,yyy);
[outputparameters, fval]=fminsearch(mx,initialparameter);


%% uniformly resample from ellipse 
t=linspace(0,2*pi,200);

xao=outputparameters(1)*cos(t);
yao=outputparameters(2)*sin(t);
a=outputparameters(3);
z=[cos(a) -sin(a);sin(a) cos(a)];
m=[xao;yao];
k=z*m;

xao=k(1,:);
yao=k(2,:);

scatter(xao,yao); 
hold on;
scatter(circle_points_x,circle_points_y,'r');
axis([-50 50 -50 50]);
axis equal;
drawnow;
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


