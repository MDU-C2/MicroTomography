clear all 
close all
clc

load surfacePoint11221058.mat


figure; hold on;
for i = 1: size(surfacePoints,3)

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
figure; hold on;
for i = 1:size(surfacePoints,3)
    scatter3(surfacePoints(:,1,i),surfacePoints(:,2,i),surfacePoints(:,3,i) )
    view(3)
    pause(1)
end

%%
spline_data = surfacePoints(:,:,3);

figure;
plot(spline_data(:,3),spline_data(:,2),'Marker','*')

