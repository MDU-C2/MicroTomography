clear all 
close all
clc

new_code = load ('SurfacePoint11231426_NecCodeEm.mat');
new_code = new_code.surfacePoint;

for i = 1:size(new_code,3)
    x = new_code(:,1,i);
    y = new_code(:,2,i);
    z = new_code(:,3,i);
    spline = createFit(new_code(:,2,i),new_code(:,3,i), false);
    title(i)
    % FOr Y i = 1 and i = 11 are linear interpolation change ti linear

    % FOr x i = 6 and 16 are linear 
    spline = createFit(new_code(:,1,i),new_code(:,3,i),true);

end
%%
    x = new_code(:,1,11);
    y = new_code(:,2,11);
    z = new_code(:,3,11);
    figure; 
    scatter(y,z)
