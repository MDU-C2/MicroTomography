clear all 
close all
clc

load surfacePoint11211333.mat


figure; hold on;
data = zeros(size(surfacePoint,1),size(surfacePoint,2),size(surfacePoint,3));

outliner = zeros(size(surfacePoint,1),size(surfacePoint,2),size(surfacePoint,3))
for i = 1: size(surfacePoint,3)
    
    first_nan = find(isnan (surfacePoint(5:end,:,i)),1, 'first');% start from value 5 as first value may be nan sometimes 
    surfacePoint(first_nan:end, : , i) = nan; 
    outliner(:,:,i) = isoutlier(surfacePoint(:,:,i), "movmedian",2);

    plot(surfacePoint(:,3,i),surfacePoint(:,2,i), 'Marker','*')
end