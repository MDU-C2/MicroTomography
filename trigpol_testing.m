clear all 
close all
clc

load surfacePoint11161346.mat


figure; hold on;
for i = 1%: size(surfacePoints,3)

   plot(surfacePoints(:,3,i),surfacePoints(:,1,i), 'Marker','*')
end
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

old = load ('angle10_surfacePoint11221058.mat');
old = old.surfacePoints;
stl_file = stlread('symmetricalBreastModel.STL');
real_points = rotx(90)*stl_file.Points';
real_points = real_points';

real_points(:,1) = real_points(:,1) -60;
real_points(:,2) = real_points(:,2) +60;
real_points(:,3) = real_points(:,3) -120;

figure; hold on;
for i = 1:size(surfacePoints,3)
    scatter3(surfacePoints(:,1,i),surfacePoints(:,2,i),surfacePoints(:,3,i), 'filled', 'black' )
    scatter3(old(:,1,i),old(:,2,i),old(:,3,i), 'filled', 'blue' )
    view(3)

end
hold on; 
scatter3(real_points(:,1),real_points(:,2),real_points(:,3),'Marker','.')
xlabel('X')
ylabel('Y')
zlabel('Z')
%%
spline_data = surfacePoints(:,:,3);

figure;
plot(spline_data(:,3),spline_data(:,2),'Marker','*')

