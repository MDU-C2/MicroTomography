clear all 
close all
clc

load surfacePoint11221018.mat


figure; hold on;
data = zeros(size(surfacePoint,1),size(surfacePoint,2),size(surfacePoint,3));

outliner = zeros(size(surfacePoint,1),size(surfacePoint,2),size(surfacePoint,3))
% for i = 1: size(surfacePoint,3)
%     
% %     first_nan = find(isnan (surfacePoint(5:end,:,i)),1, 'first');% start from value 5 as first value may be nan sometimes 
% %     surfacePoint(first_nan:end, : , i) = nan; 
% %     outliner(:,:,i) = isoutlier(surfacePoint(:,:,i), "movmedian",2);
% 
%  %   plot(surfacePoint(:,3,i),surfacePoint(:,1,i), 'Marker','*')
% end
figure; hold on;
for i = 1:size(surfacePoint,3)
    scatter3(surfacePoint(:,1,i),surfacePoint(:,2,i),surfacePoint(:,3,i) )
    view(3)
    pause(1)
end

%%
clear all 
close all
clc

load LaserPoint11221018.mat
ppoints = zeros(size(LaserPoints,1),3,size(LaserPoints,3))
for i = 1:size(LaserPoints,3)
    for j = 1:size(LaserPoints,1)
        pos = LaserPoints(j,1:3,i);
        euler = LaserPoints(j,4:6,i);
        rotm = eul2rotm(deg2rad(euler));
        HT = se3(rotm,pos);
        point_laser_base = [0,0,LaserPoints(j,7,i)];
        ppoints(j,:,i) = HT.transform(point_laser_base);

    end
    
end
figure; hold on;
for i = 1:size(ppoints,3)
    scatter3(ppoints(:,1,i),ppoints(:,2,i),ppoints(:,3,i) )
    view(3)
    pause(1)
end
