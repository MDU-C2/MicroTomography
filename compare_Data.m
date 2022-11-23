clear all 
close all
clc

light_above = load ('surfacePoint11221608_RemoveLightAbove.mat');
light_above = light_above.surfacePoints;

new_code = load ('SurfacePoint11231426_NecCodeEm.mat');
new_code = new_code.surfacePoint;


light_above_extra = load ('surfacePoint11221617_RemoveLightAboveExtra.mat');
light_above_extra = light_above_extra.surfacePoints;

no_roof = load ('surfacePoint11221523_white_10degrees_TCPChange_protect.mat');
no_roof = no_roof.surfacePoints;

no_protect = load ('surfacePoint11221446_white_10degrees_TCPChange.mat');
no_protect = no_protect.surfacePoints;

stl_file = stlread('symmetricalBreastModel.STL');
%Rotate
real_points = rotx(90)*stl_file.Points';
real_points = real_points';
% Centering
real_points(:,1) = real_points(:,1) -60;
real_points(:,2) = real_points(:,2) +60;
real_points(:,3) = real_points(:,3) -120;

d3fig = figure();



for i = 1: size(no_protect,3)
    figure(d3fig); hold on; 
    scatter3(no_protect(:,1,i),no_protect(:,2,i),no_protect(:,3,i), '+','cyan')
    scatter3(no_roof(:,1,i),no_roof(:,2,i),no_roof(:,3,i), '*','magenta')
    scatter3(light_above(:,1,i),light_above(:,2,i),light_above(:,3,i), 'x','blue')
    scatter3(light_above_extra(:,1,i),light_above_extra(:,2,i),light_above_extra(:,3,i), 'hexagram','red')
    scatter3(new_code(:,1,i),new_code(:,2,i),new_code(:,3,i), 'hexagram','black')
    hold off; 
    
    d2fig = figure(); hold on;  
    scatter(no_protect(:,3,i),no_protect(:,1,i),'cyan','+')
    scatter(no_roof(:,3,i),no_roof(:,1,i),'magenta', '*')
    scatter(light_above(:,3,i),light_above(:,1,i),'blue', 'x')
    scatter(light_above_extra(:,3,i),light_above_extra(:,1,i), 'hexagram','red')
    scatter(new_code(:,3,i),new_code(:,1,i), 'hexagram','black')
    xlabel('Z')
    ylabel('X')
    legend('no_protect', 'no_roof', 'light_above', 'light_above_extra')
    hold off

    d2fig2 = figure(); hold on;  
    scatter(no_protect(:,3,i),no_protect(:,2,i),'cyan','+')
    scatter(no_roof(:,3,i),no_roof(:,2,i),'magenta', '*')
    scatter(light_above(:,3,i),light_above(:,2,i),'blue', 'x')
    scatter(light_above_extra(:,3,i),light_above_extra(:,2,i),'red', 'hexagram')
    scatter(new_code(:,3,i),new_code(:,2,i),'red', 'black')
    xlabel('Z')
    ylabel('Y')
    legend('no_protect', 'no_roof', 'light_above', 'light_above_extra')
    hold off

end
figure(d3fig); hold on;
scatter3(real_points(:,1),real_points(:,2),real_points(:,3),'.','yellow')
legend('no_protect', 'no_roof', 'light_above', 'light_above_extra', 'real_points')
xlabel('X')
ylabel('Y')
zlabel('Z')
hold off;


figure; hold on ; 
scatter(real_points(:,3),real_points(:,1));
for i = 1:size(new_code,3)
    %scatter(new_code(:,3,i)-10, new_code(:,1,i)-3,'filled','red')
    scatter(light_above_extra(:,3,i)-10, light_above_extra(:,1,i)-3,'filled','black')
end
xlabel('Z')
ylabel('X')
legend('stl data','New code', 'old code')

figure; hold on ; 
scatter(real_points(:,3),real_points(:,2));
for i = 1:size(new_code,3)
    scatter(new_code(:,3,i)-10, new_code(:,2,i)-3,'filled','red')
    scatter(light_above_extra(:,3,i)-10, light_above_extra(:,2,i)-3,'filled','black')
end
xlabel('Z')
ylabel('Y')
legend('stl data','New code', 'old code')

%% Spline interpolation 
clear all 
close all 
clc 
% Load data 
data = load ('surfacePoint11221617_RemoveLightAboveExtra.mat');
data = data.surfacePoints;
% Choose spline 
spline_number = 5;

% X interpolation
ppx = csapi(data(:,3, spline_number), data(:,1,spline_number));

spx = spap2(1,3,data(:,3, spline_number),data(:,1,spline_number)); 
spx = spap2(newknt(spx),3,data(:,3, spline_number),data(:,1,spline_number));
spx = spap2(newknt(spx),3,data(:,3, spline_number),data(:,1,spline_number));
spx = spap2(newknt(spx),3,data(:,3, spline_number),data(:,1,spline_number));
% Plot a spline in X and Y 

figure;  hold on;
scatter(data(:,3,spline_number),data(:,1,spline_number));
fnplt(spx) 
xlabel('Z')
ylabel('X')
% figure; 
% scatter(data(:,3,spline_number),data(:,2,spline_number));
% xlabel('Z')
% ylabel('Y')





%%
figure; hold on;
for i = 1: size(surfacePoints,3)

   plot(surfacePoints(:,3,i),surfacePoints(:,2,i), 'Marker','*')
end
%%
figure; hold on;
for i = 1: size(surfacePoints,3)
   plot(surfacePoints(:,1,i),surfacePoints(:,2,i), 'Marker','*')
end
%% 
 
for i = 1: size(surfacePoints,1)
   figure;
   plot(squeeze(surfacePoints(i,2,:)),squeeze(surfacePoints(i,1,:)), 'Marker','*')
end
%%
clear all 
close all
clc

load surfacePoint11161346.mat
offset = load ('surfacePoint11221446_white_10degrees_TCPChange.mat');
offset = offset.surfacePoints;

newnew = load ('surfacePoint11221523_white_10degrees_TCPChange_protect.mat');
newnew = newnew.surfacePoints;

old = load ('angle10_surfacePoint11221058.mat');
old = old.surfacePoints;

new = load ('angle_10_low_speed_surfacePoint11221408.mat');
new = new.surfacePoints;

stl_file = stlread('symmetricalBreastModel.STL');
real_points = rotx(90)*stl_file.Points';
real_points = real_points';

real_points(:,1) = real_points(:,1) -60;
real_points(:,2) = real_points(:,2) +60;
real_points(:,3) = real_points(:,3) -120;

figure; hold on;
for i = 1:size(surfacePoints,3)
%     scatter3(surfacePoints(:,1,i),surfacePoints(:,2,i),surfacePoints(:,3,i), 'filled', 'black' )
%     scatter3(old(:,1,i),old(:,2,i),old(:,3,i), 'filled', 'blue' )
%     scatter3(new(:,1,i)-1,new(:,2,i)-3,new(:,3,i), 'filled', 'magenta' )
%     scatter3(offset(:,1,i),offset(:,2,i),offset(:,3,i), 'filled', 'red' )
     scatter3(newnew(:,1,i),newnew(:,2,i),newnew(:,3,i), 'filled', 'blue' )
%     view(3)

end

scatter3(real_points(:,1),real_points(:,2),real_points(:,3),'black')
xlabel('X')
ylabel('Y')
zlabel('Z')
legend('före nyaste data', 'Nyaste data ', 'STL data')
%%
spline_data = surfacePoints(:,:,3);

figure;
plot(spline_data(:,3),spline_data(:,2),'Marker','*')

