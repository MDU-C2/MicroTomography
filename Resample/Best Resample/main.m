clear all 
close all
clc

new_code = load ('surfacePoints0912_1219.mat');
new_code = new_code.surfacePoint;
data = new_code;

% IF THE PLOT ARE SET TO TRUE THE FUNCTUON WILL PLOT EVERYTHING AND WILL
% TAKE A LOT OF TIME AND PRODUCE A LOT OF FIGURE 
% YOU NEED TO BE PATIENT IF YOU SET THE PLOT TO TRUE
points = resample_data(data,6,0.02,false,false);

% Plot the results 
figure; hold on;
for i = 1:size(data,3)
    scatter3(data(:,1,i),data(:,2,i),data(:,3,i),'red','filled')
end
scatter3(points(:,1),points(:,2),points(:,3),'blue','filled')