clear all 
close all
clc

load surfacePoint11161346.mat


figure; hold on;
for i = 1%: size(surfacePoints,3)

   plot(surfacePoints(:,3,i),surfacePoints(:,1,i), 'Marker','*', Color = 'black')
end
hold on ; 
plot(old(:,3,1),old(:,1,1), 'Marker','*',Color='blue')
plot(new(:,3,1),new(:,1,1), 'Marker','*',Color='magenta')
% plot(real_points(:,3),real_points(:,1), 'Marker','*','red')



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

